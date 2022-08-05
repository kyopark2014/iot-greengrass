sudo /greengrass/v2/bin/greengrass-cli deployment create \
  --recipeDir ./recipes \
  --artifactDir ./artifacts \
  --merge "com.example.Subscriber=1.0.0"
  