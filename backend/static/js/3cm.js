import { ethers } from "./ethers-5.7.esm.min.js";

//! mi2ma parts below: ddd block

const height_template = document.getElementById("height").content;
const copy_height_template = document.importNode(height_template, true);

const block_template = document.getElementById("block").content;
const copy_block_template = document.importNode(block_template, true);

const app = document.getElementById("app");
const add = document.getElementById("addBtn");
const renderedItems = app.children;

//! KJ Parts below

const contract_abi = [
  "event NewBlock(bytes32, address, uint256)",
];

const contract_address = "0x9a676e781a523b5d0c0e43731313a708cb607508";
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
  // }

  const contract = new ethers.Contract(contract_address, contract_abi, provider);
  const events = await contract.queryFilter('NewBlock');
  // console.log(events);

  for(var i in events){
    console.log(events[i].topics);

    var height_container = document.getElementById(events[i].topics[3]);
    // console.log(height_container);
    if(!height_container){
      copy_height_template.querySelector("#label").textContent = events[i].topics[3].replace('0x000000000000000000000000000000000000000000000000000000000000', '');
      // copy_height_template.querySelector("#title").textContent = events[i].topics[1];
      var fargment = copy_height_template.cloneNode(true);
      // console.log(fargment.firstElementChild);
      fargment.firstElementChild.setAttribute('id', events[i].topics[3]);
      app.appendChild(fargment);
    }

    height_container = document.getElementById(events[i].topics[3]);
    const block_container = document.getElementById(events[i].topics[1]);
    console.log(events[i].topics[1], block_container);

    if(block_container){
      const vote = block_container.querySelector("#vote").textContent;
      console.log(vote);

      block_container.querySelector("#vote").textContent = (parseInt(vote)+1).toString();
    }else{
      copy_block_template.querySelector("#vote").textContent = '1';
      copy_block_template.querySelector("#title").textContent = events[i].topics[1];
      var fargment = copy_block_template.cloneNode(true);
      // console.log(fargment.firstElementChild);
      fargment.firstElementChild.setAttribute('id', events[i].topics[1]);
      height_container.querySelector('#height_blocks').appendChild(fargment);
    }  

  }

};
