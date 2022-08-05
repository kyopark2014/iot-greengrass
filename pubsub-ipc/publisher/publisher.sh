sudo /greengrass/v2/bin/greengrass-cli deployment create \
  --recipeDir $HOME/iot-greengrass/pubsub-ipc/publisher/recipes \
  --artifactDir $HOME/iot-greengrass/pubsub-ipc/publisher/artifacts \
  --merge "com.example.Publisher=1.0.0"