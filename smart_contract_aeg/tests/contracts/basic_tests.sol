// SPDX-License-Identifier: NO-LICENSE

pragma solidity ^0.8.0;

contract test1 {
    address x;
    address[] approved_recip;
    constructor() 
    {
        x = msg.sender;
    }

    modifier OnlyOwner() {
        require(msg.sender == x, "you aren't the owner");
        _;
    }
    function red_button(address recip) external {
        //fuck
        selfdestruct(payable(recip));
        //you
    }

    function blue_button() external {
        x = msg.sender;
    }

    function yellow_button(address recip) public OnlyOwner
    {
        approved_recip.push(recip);
    }

    function check_approved(address recip) private returns (bool) 
    {
        for(uint i = 0; i < approved_recip.length;)
        {
            if(recip == approved_recip[i])
                return true;
        }
        return false;
    }
    function send_money(address recip, uint256 amount) public 
    {
        require(check_approved(recip), "not authorized to send funds to recipient");
        recip.call{value: amount}("");
    }
}