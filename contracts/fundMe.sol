// SPDX-License-Identifier: MIT

pragma solidity ^0.7.1;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    // To keep track of who sent what amount
    mapping(address => uint256) public addressToAmountFunded;
    address public owner;
    address[] public funders;
    AggregatorV3Interface public priceFeed;

    // Using a constructor(fxn that gets called instantly we deploy contract) to immediately define owner
    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function Fund() public payable {
        // / $50 threshold
        //uint256 minimumUSD = 50; // * 10**18;
        //require(getConversionRate(msg.value) >= minimumUSD, "You need to spend atleast $50! ");
        // / To append the value(amount in eth) to the sender
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    // what is the ETH -> USD conversion rate? Oracles needed...
    function getPrice() public view returns (uint256) {
        (
            ,
            /*uint80 roundID*/
            int256 price, /*uint startedAt*/ /*uint timeStamp*/ /*uint80 answeredInRound*/
            ,
            ,

        ) = priceFeed.latestRoundData();
        return uint256(price);
    }

    // 1000000000
    // to convert whatever value user sends to eth amount
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        // Using 10^7 iststead of 10^8, find out why? and why I didn't get many zeros
        uint256 ethAmountinUSD = (ethPrice * ethAmount) / 100000000000000000;
        return ethAmountinUSD;
    }

    modifier onlyOwner() {
        // To require msg.sender == owner
        // we add "_;" to run the rest of the code. It can be before modifier
        require(msg.sender == owner, "funds are safu boi");
        _;
    }

    // Transfer is a fxn in solidity that we can call on any address to send eth
    function withdraw() public payable onlyOwner {
        // we send money to address of "this"(contract that we're already in)
        // wrap the msg.sender in the payable keyWord argument.
        payable(msg.sender).transfer(address(this).balance);
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            // To get the address of each funder to put into the mapping and reset it.
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }

    function getEntranceFee() public view returns (uint256) {
        // minimum USD
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }
}
