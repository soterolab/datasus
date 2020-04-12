install.packages("devtools")
install.packages("rtools")
install.packages("read.dbc")
install.packages("glue")

devtools::install_github("rfsaldanha/microdatasus")

library(microdatasus)

raw <- fetch_datasus(year_start = 1998, year_end = 2018,
                     uf = "all", information_system = "SIM-DOEXT")
df <- process_sim(data = raw)

write.csv(df, file = "datasus.csv", fileEncoding = "UTF-8", na = "")
