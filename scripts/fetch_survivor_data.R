library(survivoR)
library(arrow)  # For saving to Parquet

# Load the datasets from the survivoR package
castaways <- survivoR::castaways
episodes <- survivoR::episodes
# Add other datasets later...

# Write them to the raw data directory in Parquet format
write_parquet(castaways, "../data/raw/castaways.parquet")
write_parquet(episodes, "../data/raw/episodes.parquet")
