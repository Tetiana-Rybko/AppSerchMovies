from connector_mysql import DatabaseManager
from search_movies import FilmSearch
from queries_histoire import SearchHistory
from dotenv import load_dotenv
import os

load_dotenv()

def main():

    db_manager = DatabaseManager(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

    film_search = FilmSearch(db_manager)

    history = SearchHistory()

    print("Добро пожаловать в приложение для поиска фильмов!")
    print("Доступные команды:")
    print("  1 - Поиск по ключевому слову")
    print("  2 - Поиск по жанру и году")
    print("  3 - Вывести самые популярные запросы")
    print("  exit - Выход из приложения")

    while True:
        command = input("\nВведите команду: ").strip()
        if command == "exit":
            print("Выход из приложения.")
            break

        elif command == "1":
            keyword = input("Введите ключевое слово для поиска: ").strip()
            # Сохраняем запрос в истории
            history.save_query(f"keyword: {keyword}")
            results = film_search.search_by_keyword(keyword)
            if results:
                print("\nНайденные фильмы:")
                for film in results:
                    print(f"  {film['title']} ({film['release_year']})")
            else:
                print("Фильмы не найдены.")

        elif command == "2":
            genre = input("Введите жанр: ").strip()
            year = input("Введите год выпуска: ").strip()
            # Сохраняем запрос в истории
            history.save_query(f"genre: {genre}, year: {year}")
            results = film_search.search_by_genre_and_year(genre, year)
            if results:
                print("\nНайденные фильмы:")
                for film in results:
                    print(f"  {film['title']} ({film['release_year']}), жанр: {film['category']}")
            else:
                print("Фильмы не найдены.")

        elif command == "3":
            popular = history.get_popular_queries()
            if popular:
                print("\nПопулярные запросы:")
                for row in popular:
                    print(f"  {row[0]} – {row[1]} раз(а)")
            else:
                print("История запросов пуста.")

        else:
            print("Неизвестная команда. Пожалуйста, попробуйте ещё раз.")

        # Закрываем подключения к базам данных
    db_manager.close()
    history.close()


if __name__ == '__main__':
    main()