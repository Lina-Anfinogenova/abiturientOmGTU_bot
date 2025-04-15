from config import secrets
from supabase import Client, create_client

import math

class UserDataRepository:
    def __init__(self):
        # Инициализация клиента
        self.supabase: Client = create_client(secrets.SUPABASE_URL, secrets.SUPABASE_KEY)

        self.ITEMS_PER_PAGE = 5 # Количество элементов на странице

    def getAllFaculties(self):
        # Получение списка всех факультетов
        return self.supabase.table("faculties").select("*").execute().data

    def getFacultyById(self, id_faculty,  page: int = 0):
        return self.supabase.table("faculties").select("*").eq("id_faculty", str(id_faculty)).execute().data[0]

    def getSpecialityByIdFaculty(self, id_faculty: int, page: int = 0):
        """Получение специальностей с пагинацией"""
        start = page * self.ITEMS_PER_PAGE
        end = start + self.ITEMS_PER_PAGE - 1

        # Получаем общее количество
        count = self.supabase.table("specialties") \
            .select("id_speciality", count="exact") \
            .eq("id_faculty", id_faculty) \
            .execute().count

        # Получаем данные для страницы
        data = self.supabase.table("specialties") \
            .select("*") \
            .eq("id_faculty", id_faculty) \
            .range(start, end) \
            .execute()

        total_pages = math.ceil(count / self.ITEMS_PER_PAGE)
        return data.data, total_pages

    def getSpecById(self, spec_id):
        return self.supabase.table("specialties")\
            .select("*")\
            .eq("id_speciality", spec_id)\
            .execute()\
            .data[0]

userDataRepository = UserDataRepository()