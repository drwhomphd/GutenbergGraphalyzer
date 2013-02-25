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

avgivd = c()
avgsi = c()

sdivd = c()
sdsi = c()

counts = c()

for(e in seq(20, 1971, 10)){
  qry = sprintf("SELECT DISTINCT(ab.etextID), exp.* FROM experiments exp, authordetails ad, bookauthors ab, ebooks eb WHERE ad.authorID = ab.authorID AND ab.etextID = eb.etextID AND CAST(ad.birth AS INTEGER) >= %d AND CAST(ad.birth AS INTEGER) < %d AND exp.etextID = ab.etextID", e, e+10)
  tbl = dbGetQuery(con, qry)
  avgivd = c(avgivd, mean(tbl$ivdnorm))
  sdivd = c(sdivd, sd(tbl$ivdnorm))
  avgsi = c(avgsi, mean(tbl$sinorm))
  sdsi = c(sdsi, mean(tbl$sinorm))

  qry = sprintf("SELECT COUNT(DISTINCT(ab.etextID)), exp.* FROM experiments exp, authordetails ad, bookauthors ab, ebooks eb WHERE ad.authorID = ab.authorID AND ab.etextID = eb.etextID AND CAST(ad.birth AS INTEGER) >= %d AND CAST(ad.birth AS INTEGER) < %d AND exp.etextID = ab.etextID", e, e+10)
  
  tbl2 = dbGetQuery(con, qry)
  counts = c(counts, tbl2[,1])
}

plot(counts~seq(20, 1971, 10), type="l", xlab="Author Birth Year", ylab="Ebook Count", main = "Ebook Count Per Author Birth Decade (AD)")

plot(avgsi~seq(20,1971, 10), type="l", xlab="Author Birth Decade(AD)", ylab="Bits", main = "Complexity of Literature")
lines(seq(20,1971, 10), avgivd, col="red")

#tbl = dbGetQuery(con, "SELECT * FROM experiments exp, authordetails ad, bookauthors ab, ebooks eb WHERE ad.authorID = ab.authorID AND ab.etextID = eb.etextID AND CAST(ad.birth AS INTEGER) >= 1820 AND CAST(ad.birth AS INTEGER) < 1830 AND exp.etextID = ab.etextID")

#pairs(tbl)


