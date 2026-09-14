# =========== install and load the package ===========
#install.packages("AmesHousing")

library(AmesHousing)

# =========== load processed dataset ===========
ames_housing_processed <- make_ames()

# =========== save as csv ===========
write.csv(ames_housing_processed, "ames_housing.csv", row.names=FALSE)