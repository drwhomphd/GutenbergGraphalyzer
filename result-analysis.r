library(RSQLite)
library(ggplot2)

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

avgs = c()
sds = c()

for(e in seq(1500, 1980, 5)){
  qry = sprintf("SELECT * FROM experiments exp, authordetails ad, bookauthors ab, ebooks eb WHERE ad.authorID = ab.authorID AND ab.etextID = eb.etextID AND CAST(ad.birth AS INTEGER) >= %d AND CAST(ad.birth AS INTEGER) < %d AND exp.etextID = ab.etextID", e, e+10)
  tbl = dbGetQuery(con, qry)
  avgs = c(avgs, mean(tbl$da))
  sds = c(sds, sd(tbl$da))
}

plot(avgs~seq(1500, 1980, 5), type="l")


tbl = dbGetQuery(con, "SELECT * FROM experiments exp, authordetails ad, bookauthors ab, ebooks eb WHERE ad.authorID = ab.authorID AND ab.etextID = eb.etextID AND CAST(ad.birth AS INTEGER) >= 1820 AND CAST(ad.birth AS INTEGER) < 1830 AND exp.etextID = ab.etextID")

#pairs(tbl)


