const path = require("path");
require('dotenv').config({path: './.env'});
const HDWalletProvider = require("@truffle/hdwallet-provider");
var Web3 = require('web3');

var test_url = "wss://apis.ankr.com/wss/90c54dabfa2d472f9561d831eb6279b9/da0b9aaebd5cd36c8aba4042497a095a/binance/full/test"
var test_user = process.env.TEST_WSS_USER
var test_password = process.env.TEST_WSS_PASSWORD

const test_bsc_web3Provider = new Web3.providers.WebsocketProvider(test_url, {
 headers: { authorization: `Basic ${Buffer.from(`${test_user}:${test_password}`).toString('base64')}`}
})

var main_url = "wss://apis.ankr.com/wss/459efe50fc5945288f4df94dc732094d/da0b9aaebd5cd36c8aba4042497a095a/binance/full/main"
//var main_url = "wss://bsc.getblock.io/mainnet/?api_key=978baa33-7d71-4b05-89f3-436c426d04b9"
var main_user = process.env.MAIN_WSS_USER
var main_password = process.env.MAIN_WSS_PASSWORD

const main_bsc_web3Provider = new Web3.providers.WebsocketProvider(main_url, {
 headers: { authorization: `Basic ${Buffer.from(`${main_user}:${main_password}`).toString('base64')}`}
})

module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // to customize your Truffle configuration!
  plugins: [
    'truffle-plugin-verify'
  ],
  api_keys: {
    etherscan: process.env.ETHERSCAN_API,
    bscscan: process.env.BSC_API
  },
  contracts_build_directory: path.join(__dirname, "vapp/src/contracts"),
  compilers: {
    solc: {
      version: ">=0.6.0 <0.8.0",
      settings: {
        optimizer: {
          enabled: true,
          runs: 200   // Optimize for how many times you intend to run the code
        }
      }
    }
  },
  networks: {
    develop: {
      port: 8545,
      defaultEtherBalance: 100000,
    },
    mumbai: {
      provider: function() {
        return new HDWalletProvider(process.env.PRIVATE_KEY, "wss://rpc-mumbai.maticvigil.com/ws")
      },
      network_id: 80001,
    },
    rinkeby: {
      provider: () => new HDWalletProvider(process.env.PRIVATE_KEY, "wss://rinkeby.infura.io/ws/v3/ba540ca359744e14a31171bc87df6ea4"),
      network_id: 4,
      skipDryRun: true,
    },
    ganache_local: {
      host: "localhost",
      port: 7545,
      network_id: "5777"
    },
    binance_test: {
      provider: () => new HDWalletProvider(process.env.PRIVATE_KEY, "wss://data-seed-prebsc-1-s1.binance.org:8545" /*"https://data-seed-prebsc-1-s1.binance.org:8545"*/ /*test_bsc_web3Provider*/),
      network_id: 97,
      confirmations: 1,
      timeoutBlocks: 200,
      skipDryRun: true,
      networkCheckTimeout: 1000000,
      gas: 7000000,
      gasPrice: 10000000000 // 6 gwei
    },
    binance_main: {
      provider: () => new HDWalletProvider(process.env.PRIVATE_KEY, "wss://old-small-wildflower.bsc.quiknode.pro/83a210b15a3a4d829e3d4415875523251419fbd0/"),
      network_id: 56,
      confirmations: 1,
      timeoutBlocks: 200,
      skipDryRun: true,
      networkCheckTimeout: 1000000,
      gas: 8000000,
      gasPrice: 10000000000 // 6 gwei
    },
    mainnet: {
      provider: () => new HDWalletProvider(process.env.PRIVATE_KEY, "wss://mainnet.infura.io/ws/v3/ba540ca359744e14a31171bc87df6ea4"),
      gas: 8000000,
      gasPrice: 75000000000, // 60 gwei
      network_id: 1,
      skipDryRun: true,
    }
  },
};