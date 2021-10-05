from types import prepare_class
import psycopg2

db = psycopg2.connect("dbname=news")

curr = db.cursor()

text_1 = "What are the most popular three articles of all time? \n\
        \t {}\n\
        \t {}\n\
        \t {}\n"

text_2 = "Who are the most popular article authors of all time? \n\
          \t {}\n\
          \t {}\n\
          \t {}\n\
          \t {}\n"

text_3 = "On which days did more than 1% of requests lead to errors? \n\
          \t {}"

first_query = "SELECT title \
               FROM articles \
               WHERE slug IN \
                            (SELECT SUBSTRING(path,10) \
                            FROM (SELECT path , COUNT(id) \
                                FROM log \
                                WHERE path != '/' \
                                GROUP BY path \
                                ORDER BY 2 DESC \
                                LIMIT 3) AS T1 \
                            LIMIT 3);" 

second_query = "SELECT popularity \
                FROM (SELECT path , COUNT(id) AS popularity \
                     FROM log \
                     WHERE path != '/' \
                     GROUP BY path \
                     ORDER BY 2 DESC \
                     LIMIT 3) AS T1 \
                LIMIT 3;"

third_query = "SELECT aut.name , COUNT(*) AS total  \
               FROM authors aut JOIN articles art ON aut.id = art.author \
               JOIN log l ON SUBSTRING(l.path,10) = art.slug \
               GROUP BY 1 \
               ORDER BY 2 DESC \
               LIMIT 4;"


fourth_query = "SELECT DATE_TRUNC('day',time) , COUNT(status) \
                FROM log \
                WHERE status LIKE '4%' OR status LIKE '5%' \
                GROUP BY 1 \
                ORDER BY 1;"

fifth_query = "SELECT DATE_TRUNC('day',time) , COUNT(status) \
                FROM log \
                GROUP BY 1 \
                ORDER BY 1;"


curr.execute(first_query)
result_1 = curr.fetchall()

curr.execute(second_query)
result_2 = curr.fetchall()
result_2 = [str(x[0]) for x in  result_2]

curr.execute(third_query)
result_3 = curr.fetchall()
result_3 = [ (x[0],str(x[1]) ) for x  in result_3]

curr.execute(fourth_query)
result_4 = curr.fetchall()

curr.execute(fifth_query)
result_5 = curr.fetchall()


result_6 = [( str( result_5[x][0].date() ) , 100*result_4[x][1]/result_5[x][1] ) for x in range(len(result_5)) if 100*result_4[x][1]/result_5[x][1] > 1 ]


with open('output.txt','w') as file:
    file.write(text_1.format(result_1[0][0] + "   -   " + result_2[0] + " views",result_1[1][0] + "   -   " + result_2[1] + " views",result_1[2][0] + "   -   " + result_2[2] + " views" ))
    file.write(text_2.format(result_3[0][0] + "   -   " + result_3[0][1] + " views",result_3[1][0] + "   -   " + result_3[1][1] + " views",result_3[2][0] + "   -   " + result_3[2][1] + " views",result_3[3][0] + "   -   " + result_3[3][1] + " views"))
    file.write(text_3.format(result_6[0][0]) + "   -   " + str(result_6[0][1])[:4])
