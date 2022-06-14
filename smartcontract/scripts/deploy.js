require("@nomiclabs/hardhat-ethers");

module.exports = {
  networks: {
    defaultNetwork: "mumbai",
    hardhat: {
    },
    mumbai: {
      url: "https://polygon-mumbai.g.alchemy.com/v2/Yhxph16ZcUI-mMhwVyS9p3R1g45fcuIu",
      accounts: ['0xab5694775b36b4cC86E5288f4a6A906C82C8EF1C']
    }
  },
  solidity: {
    version: "0.8.0",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  },
  mocha: {
    timeout: 20000
  }
}
