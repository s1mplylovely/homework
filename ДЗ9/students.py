import asyncio
import csv
from typing import Any
from sqlalchemy import Column, String, Integer, select, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    course = Column(String, nullable=False)
    mark = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Фамилия - {self.surname}, имя - {self.name}, факультет - {self.department}, курс - {self.course}, оценка - {self.mark}"

    def to_dict(self) -> dict[str, Any]:
        return {
            'Фамилия': self.surname,
            'Имя': self.name,
            'Факультет': self.department,
            'Курс': self.course,
            'Оценка': self.mark
        }


class StudentDB:
    def __init__(self, db_url: str) -> None:
        self.engine = create_async_engine(db_url, echo=False)
        self.Session = sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    async def create_db(self) -> None:
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def clear_db(self) -> None:
        async with self.engine.begin() as connection:
            await connection.execute(text(f'TRUNCATE TABLE "students" RESTART IDENTITY CASCADE;'))

    async def add_student(self, student: Student) -> None:
        async with self.Session() as session:
            session.add(student)
            await session.commit()

    async def add_students(self, students_data: dict) -> None:
        async with self.Session() as session:
            students = []
            for data in students_data:
                student = Student(**data)
                students.append(student)
            session.add_all(students)
            await session.commit()

# метод для заполнения модели данными из файла
    async def load_from_csv(self, filename: str) -> None:
        with open(filename,  mode='r', newline='', encoding='utf-8') as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            next(data)
            async with self.Session() as session:
                for line in data:
                    student = Student(
                        surname=line[0],
                        name=line[1],
                        department=line[2],
                        course=line[3],
                        mark=int(line[4])
                    )
                    session.add(student)
                await session.commit()

# метод для получения списка студентов по названию факультета
    async def get_by_department(self, department: str) -> list[str]:
        async with self.Session() as session:
            result = await session.execute(
                select(Student.surname + " " + Student.name).where(
                    Student.department == department).distinct(Student.surname, Student.name)
            )
            return result.scalars().all()

# метод для получения списка уникальных курсов
    async def get_courses(self) -> list[str]:
        async with self.Session() as session:
            result = await session.execute(
                select(Student.course).distinct()
            )
            # return [row[0] for row in result.all()]
            return result.scalars().all()

# метод для получения среднего балла по факультету
    async def get_mean_grade(self, department: str) -> int:
        async with self.Session() as session:
            result = await session.execute(
                select(Student.mark).where(Student.department == department)
            )
            grades = result.scalars().all()
            return sum(grades)/len(grades)

# метод для получения списка студентов по выбранному курсу с оценкой ниже 30 баллов
    async def get_by_course_and_grade(self, course: str, mark: int) -> list[str]:
        async with self.Session() as session:
            result = await session.execute(
                select(Student.surname + " " + Student.name).where(Student.course ==
                                                                   course, Student.mark < mark).distinct(Student.surname, Student.name)
            )
            return result.scalars().all()


async def main():
    db = StudentDB(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/students_db")
    await db.create_db()
    # await db.load_from_csv("students.csv")
    # await db.clear_db()
    print("Студенты факультета АВТФ:")
    res = await db.get_by_department('АВТФ')
    print('\n'.join(res))
    print("\nСписок уникальных курсов:")
    res = await db.get_courses()
    print('\n'.join(res))
    print("\nСредний балл по факультету ФТФ:")
    res = await db.get_mean_grade("ФТФ")
    print(round(res, 3))
    print("\nСписок студентов по курсу 'Теор. Механика' с оценкой ниже 30 баллов:")
    res = await db.get_by_course_and_grade("Теор. Механика", 30)
    print('\n'.join(res))

if __name__ == "__main__":
    asyncio.run(main())
