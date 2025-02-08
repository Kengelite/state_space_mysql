import mysql.connector
import sys
sys.stdout.reconfigure(encoding='utf-8')
# 📌 ฟังก์ชันเชื่อมต่อ MySQL
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",   # เปลี่ยนเป็นชื่อผู้ใช้ MySQL ของคุณ
        password="",   # เปลี่ยนเป็นรหัสผ่าน MySQL ของคุณ
        database="state_space"  # เปลี่ยนเป็นชื่อฐานข้อมูลที่ต้องการใช้
    )

# 📌 ฟังก์ชันอ่านไฟล์และบันทึกข้อมูลลง MySQL
def process_file(filename):
    conn = connect_to_db()
    cursor = conn.cursor()

    state_map = {}  # เก็บ state → id
    transition_map = {}  # เก็บ transition → id

    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 3:
                continue  # ข้ามบรรทัดที่มีรูปแบบผิด

            start_state, end_state, transition = parts

            #  แทรก start_state ถ้ายังไม่มี
            if start_state not in state_map:
                cursor.execute("INSERT IGNORE INTO state (name) VALUES (%s)", (start_state,))
                conn.commit()
                cursor.execute("SELECT id FROM state WHERE name = %s", (start_state,))
                result = cursor.fetchall()  #  แก้ไข: ใช้ fetchall() เพื่อดึงข้อมูลทั้งหมด
                if result:
                    state_map[start_state] = result[0][0]

            #  แทรก end_state ถ้ายังไม่มี
            if end_state not in state_map:
                cursor.execute("INSERT IGNORE INTO state (name) VALUES (%s)", (end_state,))
                conn.commit()
                cursor.execute("SELECT id FROM state WHERE name = %s", (end_state,))
                result = cursor.fetchall()  #  แก้ไข: ใช้ fetchall() เพื่อดึงข้อมูลทั้งหมด
                if result:
                    state_map[end_state] = result[0][0]

            #  แทรก transition ถ้ายังไม่มี
            if transition not in transition_map:
                cursor.execute("INSERT IGNORE INTO transition (name) VALUES (%s)", (transition,))
                conn.commit()
                cursor.execute("SELECT id FROM transition WHERE name = %s", (transition,))
                result = cursor.fetchall()  # แก้ไข: ใช้ fetchall() เพื่อดึงข้อมูลทั้งหมด
                if result:
                    transition_map[transition] = result[0][0]

            #  เพิ่มข้อมูลลงตาราง graph
            cursor.execute("""
                INSERT INTO graph (start_state, end_state, id_trasition)
                VALUES (%s, %s, %s)
            """, (state_map[start_state], state_map[end_state], transition_map[transition]))
            conn.commit()

    cursor.close()
    conn.close()
    print(" อัปโหลดข้อมูลลงตาราง graph สำเร็จ!")

# ✅ เรียกใช้ฟังก์ชันโดยระบุไฟล์ที่ต้องการอ่าน
process_file("C:/cpntool-cha/model_test_all/trans-ex2.txt")

