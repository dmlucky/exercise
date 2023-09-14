import sqlite3

# 1. 从文件中读取内容到列表
with open('stephen_king_adaptations.txt', 'r') as file:
    stephen_king_adaptations_list = file.readlines()

# 2. 建立数据库连接
conn = sqlite3.connect('stephen_king_adaptations.db')
cursor = conn.cursor()

# 3. 创建表
cursor.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
                  movieID INTEGER PRIMARY KEY,
                  movieName TEXT,
                  movieYear INTEGER,
                  imdbRating REAL
                )''')

# 4. 插入或更新数据
for line in stephen_king_adaptations_list:
    movie_data = line.strip().split(',')
    if len(movie_data) == 4:
        movie_name = movie_data[1]
        movie_year = movie_data[2]
        imdb_rating = movie_data[3]
        if movie_year.isdigit():  # 检查电影年份是否是数字
            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName = ?", (movie_name,))
            existing_movie = cursor.fetchone()
            if existing_movie:
                cursor.execute("UPDATE stephen_king_adaptations_table SET movieYear = ?, imdbRating = ? WHERE movieName = ?",
                               (int(movie_year), float(imdb_rating), movie_name))
            else:
                cursor.execute("INSERT INTO stephen_king_adaptations_table (movieName, movieYear, imdbRating) VALUES (?, ?, ?)",
                               (movie_name, int(movie_year), float(imdb_rating)))
            conn.commit()
        else:
            print(f"Skipping invalid entry: {movie_name}, {movie_year}, {imdb_rating}")

# 5. 用户交互
while True:
    results = []  # 清空查询结果
    print("\nOptions:")
    print("1. Search by movie name")
    print("2. Search by movie year")
    print("3. Search by movie rating")
    print("4. STOP")
    choice = input("Enter your choice: ")

    if choice == '1':
        movie_name = input("Enter the movie name to search: ")
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName = ?", (movie_name,))
        result = cursor.fetchone()
        if result:
            print(f"Movie Name: {result[1]}")
            print(f"Movie Year: {result[2]}")
            print(f"IMDB Rating: {result[3]}")
        else:
            print("No such movie exists in our database")

    elif choice == '2':
        movie_year = input("Enter the movie year to search: ")
        if movie_year.isdigit():  # 检查输入是否为数字
            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear = ?", (int(movie_year),))
            results = cursor.fetchall()
            if results:
                print("\nSearch Results:")
                for result in results:
                    print(f"Movie Name: {result[1]}")
                    print(f"Movie Year: {result[2]}")
                    print(f"IMDB Rating: {result[3]}")
            else:
                print("No movies were found for that year in our database")
        else:
            print("Invalid year format. Please enter a valid year.")

    elif choice == '3':
        rating_limit = input("Enter the minimum IMDB rating: ")
        if rating_limit.replace(".", "", 1).isdigit():  # 检查输入是否为数字或浮点数
            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?", (float(rating_limit),))
            results = cursor.fetchall()
            if results:
                print("\nSearch Results:")
                for result in results:
                    print(f"Movie Name: {result[1]}")
                    print(f"Movie Year: {result[2]}")
                    print(f"IMDB Rating: {result[3]}")
            else:
                print("No movies at or above that rating were found in the database")
        else:
            print("Invalid rating format. Please enter a valid rating.")

    elif choice == '4':
        break

    results = []  # 清空查询结果

# 关闭数据库连接
conn.close()
