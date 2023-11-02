library(tidyr)
library(dplyr)


# Food_nutrient contains fdc_id and nutrient_id. Want to convert nutrient_id to nutrient and make it into columns via pivot wider
food_nutrient <- read.csv("Raw_Data/food_nutrient.csv")

# Nutrient contains IDs and nutrient. USE TO GET NUTRIENT NAMES
nut_names <- read.csv("Raw_Data_2/nutrient.csv")

# Food names
food_names <- read.csv("Raw_Data/food.csv")

food_amounts <- read.csv("Raw_Data/food_portion.csv")

names(nut_names)[names(nut_names)=="id"] <- "nutrient_id"
food_with_nut_names <- merge(food_nutrient, nut_names, by = "nutrient_id", all = F)    

named_data <- merge(food_with_nut_names, food_names, by = "fdc_id", all = F) 

named_data2 <- merge(named_data, food_amounts, by = "fdc_id", all = F)

# Get number of unique foods with complete data
summarize(named_data2, unique = n_distinct(description))
# Have 88 different foods

unique(named_data2$description)

# Just want to get data for now, not necessarily the one with the most data points
useful_data <- select(named_data, c(''))