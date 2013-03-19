library(RSQLite)
library(ggplot2)
library(Hmisc)

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
  sdsi = c(sdsi, sd(tbl$sinorm))


  qry = sprintf("SELECT COUNT(DISTINCT(ab.etextID)), exp.* FROM experiments exp, authordetails ad, bookauthors ab, ebooks eb WHERE ad.authorID = ab.authorID AND ab.etextID = eb.etextID AND CAST(ad.birth AS INTEGER) >= %d AND CAST(ad.birth AS INTEGER) < %d AND exp.etextID = ab.etextID", e, e+10)
  
  tbl2 = dbGetQuery(con, qry)
  counts = c(counts, tbl2[,1])
}

# Plot the book count #########################

plot(counts~seq(20, 1971, 10), type="l", xlab="Author Birth Year", ylab="Ebook Count", main = "Ebook Count Per Author Birth Decade (AD)")


# Plot ivd-norm and si-norm complexity #########

plot(avgsi~seq(20,1971, 10), type="l", xlab="Author Birth Decade(AD)", ylab="Bits", main = "Complexity of Literature")
lines(seq(20,1971, 10), avgivd, col="red")
legend("topleft", legend = c("sinorm", "ivdnorm"), col = c("black", "red"), lty = c(1, 1))

# Zoom in to 1500-1971  #########################

avgivd = c()
avgsi = c()
avgda = c()
avgaec = c()
avgnec = c()

sdivd = c()
sdsi = c()
sdda = c()
sdaec = c()
sdnec = c()

counts = c()

for(e in seq(1500, 1971, 10)){
  qry = sprintf("SELECT DISTINCT(ab.etextID), exp.* FROM experiments exp, authordetails ad, bookauthors ab, ebooks eb WHERE ad.authorID = ab.authorID AND ab.etextID = eb.etextID AND CAST(ad.birth AS INTEGER) >= %d AND CAST(ad.birth AS INTEGER) < %d AND exp.etextID = ab.etextID", e, e+10)
  tbl = dbGetQuery(con, qry)

  avgivd = c(avgivd, mean(tbl$ivdnorm))
  sdivd = c(sdivd, sd(tbl$ivdnorm))
  
  avgsi = c(avgsi, mean(tbl$sinorm))
  sdsi = c(sdsi, sd(tbl$sinorm))

  avgda = c(avgda, mean(tbl$da))
  sdda = c(sdda, sd(tbl$da))

  avgaec = c(avgaec, mean(tbl$aec))
  sdaec = c(sdaec, sd(tbl$aec))

  avgnec = c(avgnec, mean(tbl$nec))
  sdnec = c(sdnec, sd(tbl$nec))
  
  qry = sprintf("SELECT COUNT(DISTINCT(ab.etextID)), exp.* FROM experiments exp, authordetails ad, bookauthors ab, ebooks eb WHERE ad.authorID = ab.authorID AND ab.etextID = eb.etextID AND CAST(ad.birth AS INTEGER) >= %d AND CAST(ad.birth AS INTEGER) < %d AND exp.etextID = ab.etextID", e, e+10)
  
  tbl2 = dbGetQuery(con, qry)
  counts = c(counts, tbl2[,1])
}

# Re-Plot Info Complexity and counts
plot(counts~seq(1500, 1971, 10), type="l", xlab="Author Birth Year", ylab="Ebook Count", main = "Ebook Count Per Author Birth Decade (AD)")

plot(avgsi~seq(1500,1971, 10), type="l", xlab="Author Birth Decade(AD)", ylab="Bits", main = "Complexity of Literature", ylim=c(0, max(avgsi)))
lines(seq(1500,1971, 10), avgivd, col="red")
legend("topright", legend = c("sinorm", "ivdnorm"), col = c("black", "red"), lty = c(1, 1))

#Plot AEC
plot(avgaec~seq(1500,1971, 10), type="l", xlab="Author Birth Decade(AD)", main = "Complexity of Literature", ylim=c(0,max(avgaec)))
legend("topright", legend = c("AEC"), col = c("black"), lty = c(1, 1))

#Plot NEC
plot(avgnec~seq(1500,1971, 10), type="l", xlab="Author Birth Decade(AD)", main = "Complexity of Literature", ylim=c(0,max(avgnec)))
legend("topright", legend = c("NEC"), col = c("black"), lty = c(1, 1))

#Plot DA
plot(avgda~seq(1500,1971, 10), type="l", xlab="Author Birth Decade(AD)", main = "Complexity of Literature")
legend("top", legend = c("DA"), col = c("black"), lty = c(1, 1))

# Create a pair of box plots comparing an author against all those who lived within the same period of the author.
# Previous queries were done to get author ids
# ID 674 = James Joyce
# ID 1962 = Gertrude Stein
# ID 6490 = Virginia Woolf
# ID 176 = Samuel Richardson

authors = c(674, 1962, 6490, 176)
for ( i in seq(1, length(authors))) {

  print(sprintf("Author %d\n", authors[i]))
  
  # Get information for the author
  
  qry = sprintf("SELECT exp.*, ad.* FROM experiments exp, authordetails ad, bookauthors ab, ebooks eb WHERE eb.etextID = ab.etextID AND ab.authorID = ad.authorID AND ad.authorID = %d AND exp.etextID = eb.etextID", authors[i])
  
  authortbl = dbGetQuery(con, qry)

  authorbirth = as.integer(authortbl$birth[1])
  authordeath = as.integer(authortbl$death[1])
  authorlast = authortbl$last[1]
  authorfirst = authortbl$first[1]


  # Get the information for all books not by the author during their time period
  qry = sprintf("SELECT exp.*, ad.* FROM experiments exp, authordetails ad, bookauthors ba, ebooks eb WHERE eb.etextID = ba.etextID AND ba.authorID = ad.authorID AND ad.authorID != %d AND ad.birth NOT NULL AND ad.death NOT NULL AND CAST (ad.birth AS INTEGER) >= %d AND CAST(ad.death AS INTEGER) <= %d AND CAST(ad.death AS INTEGER) > 0", authors[i], authorbirth, authordeath)
  periodtbl = dbGetQuery(con, qry)

  boxplot(authortbl$ivdnorm, periodtbl$ivdnorm, names = c(authorlast, "General"))
  title(sprintf("Complexity of %s %s Compared to Others", authorfirst, authorlast))

}



#tbl = dbGetQuery(con, "SELECT * FROM experiments exp, authordetails ad, bookauthors ab, ebooks eb WHERE ad.authorID = ab.authorID AND ab.etextID = eb.etextID AND CAST(ad.birth AS INTEGER) >= 1820 AND CAST(ad.birth AS INTEGER) < 1830 AND exp.etextID = ab.etextID")

#pairs(tbl)


