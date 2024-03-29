from fastapi import FastAPI, HTTPException
from subprocess import Popen
import asyncio
import sqlite3
from datetime import datetime

app = FastAPI()
robot_process = None

async def record_run(start_from, duration):
    conn = sqlite3.connect("robot_runs.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS runs (start_from INTEGER, start_time TIMESTAMP, duration INTEGER)")
    c.execute("INSERT INTO runs (start_from, start_time, duration) VALUES (?, ?, ?)", (start_from, datetime.now(), duration))
    conn.commit()
    conn.close()

@app.post("/start_robot/{start_from}")
async def start_robot(start_from: int):
    global robot_process
    if robot_process is None or robot_process.poll() is not None:
        robot_process = Popen(["python", "robot.py", str(start_from)])
        return {"message": "Robot started."}
    else:
        raise HTTPException(status_code=400, detail="Robot is already running.")

@app.post("/stop_robot")
async def stop_robot():
    global robot_process
    if robot_process and robot_process.poll() is None:
        robot_process.terminate()
        robot_process = None
        return {"message": "Robot stopped."}
    else:
        raise HTTPException(status_code=400, detail="No running robot.")

@app.get("/robot_runs")
async def get_robot_runs():
    conn = sqlite3.connect("robot_runs.db")
    c = conn.cursor()
    c.execute("SELECT * FROM runs")
    runs = c.fetchall()
    conn.close()
    return {"robot_runs": runs}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
