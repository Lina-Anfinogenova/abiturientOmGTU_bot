from config import supabase
import math

# Чтение данных
faculties = supabase.table("faculties").select("*").execute().data

async def getFacultyById(id_faculty,  page: int = 0):
    return supabase.table("faculties").select("*").eq("id_faculty", str(id_faculty)).execute().data[0]

# Количество элементов на странице
ITEMS_PER_PAGE = 5

async def getSpecialityByIdFaculty(id_faculty: int, page: int = 0):
    """Получение специальностей с пагинацией"""
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE - 1

    # Получаем общее количество
    count = supabase.table("specialties") \
        .select("id_speciality", count="exact") \
        .eq("id_faculty", id_faculty) \
        .execute().count

    # Получаем данные для страницы
    data = supabase.table("specialties") \
        .select("*") \
        .eq("id_faculty", id_faculty) \
        .range(start, end) \
        .execute()

    total_pages = math.ceil(count / ITEMS_PER_PAGE)
    return data.data, total_pages

    # spec = supabase.table("specialties").select("*").eq("id_faculty", str(id_faculty)).execute() # fac.data[0]["id_faculty"]
    # return spec.data
