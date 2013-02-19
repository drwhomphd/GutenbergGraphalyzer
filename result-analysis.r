library(RSQLite)

con <- dbConnect("SQLite", dbname = "results/catalog.db")

# List tables in the database
dbListTables(con)

# The dbGetQuery function allows for information gathering queries
# This should be all that's needed. The results are saved in a
# datatable with registered names for each of the colums.
# E.g. resultTable$columnName works.
#dbGetQuery(con, "Query")[1,]

tbl = dbGetQuery(con, "SELECT * FROM experiments")
print(names(tbl))

#pairs(tbl)
