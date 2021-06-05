pragma solidity >=0.7.0 <0.9.0;


contract HeightValidation {

    struct User {
        uint userid;
        uint height;
        address validator;
    }

    address public signer;

    mapping(address => User) users;

    User[] public userList;

    constructor() {
        signer = msg.sender; // 'msg.sender' is sender of current call, contract deployer for a constructor
    }

    function addUser(uint _id, uint _height, address _address) public returns (User memory){
        require(msg.sender == signer,
            "Only contract deployer can add users.");

        User storage user = users[_address];
        user.userid = _id;
        user.height = _height;
        user.validator = payable(msg.sender);

        userList.push(user);
        return users[_address];
    }

    function getHeight(address _address) public view returns (User memory){
        return users[_address];
    }

    function getUsers() public view returns (User[] memory){
        return userList;
    }
}