// SPDX-License-Identifier: NO-LICENSE

pragma solidity ^0.8.0;

contract test 
{
    address x;

    constructor() 
    {
        x = msg.sender;
    }

    function send_money(address payable recip, uint256 amt) external
    {
        require(msg.sender == x, "unauthorized");
        bool succ;
        (succ, ) = recip.call{value: amt}("");
        require(succ, "couldn't send money");
    }

    function change_owner(address new_owner) external
    {
        x = new_owner;
    }
    function fuweoiwoeiruwoeuir(address new_owner) external
    {
        x = new_owner;
    }
}