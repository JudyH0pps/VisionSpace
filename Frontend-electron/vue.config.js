module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  pluginOptions: {
    electronBuilder: {
      nodeIntegration: true,
      builderOptions: {
        // options placed here will be merged with default configuration and passed to electron-builder
        appId: 'com.ssafy.visionspace',
        win: {
          target: [
            {
              target: "nsis",
              // icon: build/'@/assets/favicon.jpg',
              arch: [
                "x64",
                "ia32"
              ]
            }
          ]
        }
      }
    }
  },
}