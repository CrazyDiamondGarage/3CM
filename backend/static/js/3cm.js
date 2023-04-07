import { ethers } from "./ethers-5.7.esm.min.js";

//! mi2ma parts below: ddd block

const template = document.getElementById("sample").content;
const copyTemplate = document.importNode(template, true);
const app = document.getElementById("app");
const add = document.getElementById("addBtn");
const renderedItems = app.children;

const addBlock = () => {
  copyTemplate.querySelector("#label").textContent = "label";
  copyTemplate.querySelector("#title").textContent = "Item name";
  copyTemplate.querySelector("#desc").textContent =
    "This could be a bit longer description that is forwarded from textarea value.";
  app.appendChild(copyTemplate.cloneNode(true));
};

//! KJ Parts below

const contract_abi = [
  "event NewBlock(bytes32 indexed, bytes32 indexed, address indexed, uint)",
  "function resolve(bytes memory handle) public view returns (address)",
  "function reverse(address user) public view returns (string memory)",
];

console.log("3cm.js loaded");
// console.log(ethers);
console.log("ethers loaded");

const contract_address = "0x5fbdb2315678afecb367f032d93f642f64180aa3";
const provider = new ethers.providers.JsonRpcProvider( 'http://127.0.0.1:8545' );
// const erc20 = new ethers.Contract(address, abi, provider);

const reg_name = document.getElementById("reg_name");
const reg_btn = document.getElementById("reg_btn");

reg_btn.onclick = (evt) => {
  console.log(reg_name.value);
  fetch(`/req`, {
    method: "POST",
    body: JSON.stringify({ name: reg_name.value }),
  });

  //!TODO: addBlock() in callback function
  addBlock();
};

window.onload = async () => {
  // if (typeof window.ethereum !== 'undefined') {
  //     console.log('MetaMask is installed!');
  //     if(window.ethereum.isConnected()){
  //     }else{
  //         const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
  //     }
  //     const rsp = await fetch(`/get_metadata?wallet=${ethereum.selectedAddress}`);
  //     metadata.value = (await rsp.json())['metadata'];
  //     console.log(ethereum.selectedAddress);
  //     ethereum_address.innerText = ethereum.selectedAddress;
  //     connect_metamask_btn.onclick = async (evt) => {
  //         const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
  //         const account = accounts[0];
  //         console.log(account);
  //         ethereum_address.innerText = account;
  //         await ethereum.request({
  //             method: "wallet_addEthereumChain",
  //             params: [{
  //                 chainId: "0x13881",
  //                 rpcUrls: ["https://endpoints.omniatech.io/v1/matic/mumbai/public"],
  //                 chainName: "Mumbai Testnet",
  //                 nativeCurrency: {
  //                     name: "MATIC",
  //                     symbol: "MATIC",
  //                     decimals: 18
  //                 },
  //                 blockExplorerUrls: ["https://mumbai.polygonscan.com"]
  //             }]
  //         });
  //         await ethereum.request({
  //             method: 'wallet_switchEthereumChain',
  //             params: [{ chainId: '0x13881' }],
  //         });
  //     }
  //     const provider = new ethers.providers.Web3Provider(window.ethereum);
  //     const signer = provider.getSigner();
      const contract = new ethers.Contract(contract_address, contract_abi, provider);
      const events = await contract.queryFilter('NewBlock');  
      console.log(events);
  //     handle_mint_btn.onclick = async (evt) => {
  //         const handle = new TextEncoder().encode(handle_mint.value);
  //         await contract.mint(handle);
  //         // await contract.mint(ethers.utils.hexlify( Array.from()));
  //     }
  //     handle_resolve_btn.onclick = async (evt) => {
  //         console.log(handle_resolve.value);
  //         const handle_bytes = new TextEncoder().encode(handle_resolve.value);
  //         const address = await contract.resolve(handle_bytes);
  //         console.log(address);
  //         handle_resolve_result.innerText = address;
  //     }
  //     handle_reverse_btn.onclick = async (evt) => {
  //         console.log(handle_reverse.value);
  //         const handle = await contract.reverse(handle_reverse.value);
  //         console.log(handle);
  //         handle_reverse_result.innerText = handle;
  //     }
  //     metadata_save_btn.onclick = async (evt) => {
  //         const rsp = await fetch(`/save_metadata?token=${jwt}&wallet=${ethereum.selectedAddress}`, {method:'POST', body: metadata.value});
  //     }
  //     metadata_verify_btn.onclick = async (evt) => {
  //         console.log(metadata.value);
  //     }
  //     metadata_generate_btn.onclick = async (evt) => {
  //         const rsp = await fetch(`/generate_metadata_root?token=${jwt}`, {method:'POST', body: metadata.value});
  //     }
  // }
};
