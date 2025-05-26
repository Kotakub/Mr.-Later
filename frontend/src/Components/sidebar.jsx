import React from 'react'

export default function Sidebar() {
    return (
        <header>
            <ul className="nav">
                <li>Расписание</li>
                <li>Список</li>
                <li>Профиль</li>
            </ul>
            <div className="button_area">
                <OrangeButton text="ЗАПИСАТЬСЯ" />
                <GreenButton text="ВОЙТИ" onClick={() => setModal(true)} />
            </div>
        </header>
    )
}
