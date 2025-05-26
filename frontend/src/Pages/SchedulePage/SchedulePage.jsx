import React, { useState, useEffect } from 'react'
import './SchedulePage.css';

export default function SchedulePage() {
    const [schedule, setSchedule] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchSchedule = async () => {
            try {
                const response = await fetch('http://localhost:8000/schedule/get_schedule');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setSchedule(data);
            } catch (err) {
                setError(err.message);
                console.error('Error fetching schedule:', err);
            }
        };

        fetchSchedule();
    }, []);

    if (error) return <div>Error: {error}</div>;
    if (!schedule) return <div>Loading...</div>;

    // Вариант 1: Отображение в виде форматированного JSON (для отладки)
    return (
        <div>
            <h1>Schedule Details</h1>
            <pre>{JSON.stringify(schedule, null, 2)}</pre>
        </div>

    );
}

