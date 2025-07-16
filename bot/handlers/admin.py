from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from ..texts import *
from ..keyboards import *
from ..states import House
from ..dicts import *
from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder
from aiogram.fsm.storage.base import StorageKey
from ..db.models import *
from ..db.database import *
from ..config import *
import logging


admin = Router()

@admin.message(Command("admin"))
async def admin_start(message: Message, state: FSMContext):
    if message.from_user.id in ADMIN_LIST:
        await state.clear()
        await message.answer(text="Вы в админке выберите действие", parse_mode="HTML", reply_markup=admin_start_kb, disable_web_page_preview=True)

@admin.callback_query(ApplicationCallback.filter(F.application_id == 0))
async def admin_app(callback: CallbackQuery, callback_data: ApplicationCallback, state: FSMContext):
    if callback.from_user.id in ADMIN_LIST:
        status = callback_data.status
        page = callback_data.page
        offset = (page - 1) * 10
        applications, total = await get_applications(status=status, offset=offset)
        status_name = STATUS_MAP.get(status, status)
        
        if applications:
            kb = get_applications_kb(applications, status, page, total)
            await callback.message.edit_text(
                text=f"{status_name} (Страница {page} из {(total + 9) // 10}):",
                reply_markup=kb
            )
        else:
            await callback.message.edit_text(
                text=f"Нет заявок со статусом {status_name}",
                reply_markup=admin_start_kb
            )
        await state.update_data(current_status=status, current_page=page)
    else:
        await callback.answer("У вас нет прав для этого действия.")

@admin.callback_query(ViewApplicationCallback.filter())
async def show_application_details(callback: CallbackQuery, callback_data: ViewApplicationCallback, state: FSMContext):
    if callback.from_user.id in ADMIN_LIST:
        application_id = callback_data.application_id
        async with async_session() as session:
            result = await session.execute(select(Application).where(Application.id == application_id))
            application = result.scalars().first()

        if application:
            user_contact = await get_user_contact_info(application.user_id)
            details = (
                f"📄 <b>Заявка №{application.id}</b>\n"
                f"👤 Пользователь: {application.username_app}\n"
                f"🔗 Контакт: {user_contact}\n"
                f"🏠 Тип дома: {application.house_chosen}\n"
                f"📐 Площадь: {application.house_square}\n"
                f"🌳 Участок: {application.plot}\n"
                f"💰 Бюджет: {application.budget}\n"
                f"🕒 Сроки: {application.temp}\n"
                f"💬 Комментарий: {application.comment or 'Отсутствует'}\n"
                f"📞 Телефон: {application.phone}\n"
                f"📌 <b>Статус: {STATUS_MAP.get(application.status, application.status)}</b>\n"
                f"🗓 Дата подачи заявки: {application.registration_time.strftime('%d.%m.%Y %H:%M:%S')}"
            )

            data = await state.get_data()
            current_status = data.get("current_status", callback_data.status)
            current_page = data.get("current_page", callback_data.page)

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Принять",
                            callback_data=UpdateApplicationStatusCallback(
                                status="accepted",
                                application_id=application_id,
                                page=current_page
                            ).pack()
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="Назад",
                            callback_data=ApplicationCallback(
                                status=current_status,
                                application_id=0,
                                page=current_page
                            ).pack()
                        )
                    ]
                ]
            )

            await callback.message.edit_text(text=details, reply_markup=keyboard, parse_mode="HTML", disable_web_page_preview=True)
        else:
            await callback.message.edit_text("Заявка не найдена", reply_markup=admin_start_kb)
    else:
        await callback.answer("У вас нет прав для этого действия.")

@admin.callback_query(UpdateApplicationStatusCallback.filter())
async def update_application_status(callback: CallbackQuery, callback_data: UpdateApplicationStatusCallback, state: FSMContext):

    if callback.from_user.id not in ADMIN_LIST:
        await callback.answer("У вас нет прав для этого действия.")
        return

    application_id = callback_data.application_id
    new_status = callback_data.status

    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Application).where(Application.id == application_id)
            )
            application = result.scalars().first()

            if not application:
                await callback.answer("Заявка не найдена")
                return

            if application.status == new_status:
                await callback.answer("Заявка уже имеет этот статус.")
                return

            application.status = new_status
            await session.commit()

    await callback.answer("Статус заявки обновлён ✅")

    await show_application_details(
        callback,
        ViewApplicationCallback(
            application_id=application_id,
            page=callback_data.page,
            status=new_status
        ),
        state
    )