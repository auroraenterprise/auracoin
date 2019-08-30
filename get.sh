#!/bin/bash

clear

echo "Please wait..."

wget https://aur.xyz/auracoin/ascii.txt &> /dev/null

clear
echo -e "\e[96m"

cat ascii.txt

rm ascii.txt

echo -e "\e[1mAuracoin Setup [BETA]"
echo -e "\e[0m"
echo "This script installs Auracoin on your device."
echo "It is recommended for you to install Auracoin on Debian or Ubuntu only."
echo "If you wish to install Auracoin on another Linux distribution or different"
echo "platform entirely, please visit Auracoin's GitHub repo:"
echo ""
echo "https://github.com/auroraenterprise/auracoin"
echo ""
echo "Please note that this script is in beta, so bugs are expected. Report them"
echo "by creating a new issue on our repo above!"
echo ""
read -p "Do you wish to continue setup? [Y/n]" -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    pushd . &> /dev/null

    echo "Checking superuser privileges..."
    sudo echo "Superuser working!"

    echo "Installing git... [1/7]"
    sudo apt-get install git &> /dev/null

    echo "Installing nano... [2/7]"
    sudo apt-get install nano &> /dev/null

    echo "Installing python3... [3/7]"
    sudo apt-get install python3 &> /dev/null
    
    echo "Cloning Auracoin repository... [4/7]"
    git clone https://github.com/auroraenterprise/auracoin.git &> /dev/null
    cd auracoin

    echo "Installing dependency ecdsa... [5/7]"
    sudo python3 -m pip install ecdsa &> /dev/null
    python3 -m pip install ecdsa --user &> /dev/null

    echo "Starting Auracoin for the first time... [6/7]"
    python3 main.py -v

    if [ ! -f ~/.auracoin/config.auc ]; then
        echo "Configuration file not created, creating manually..."
        cd ~
        mkdir .auracoin

        popd
        cd auracoin/config

        cp config.auc ~/.auracoin/config.auc
    fi

    echo "Opening configuration file... [7/7]"
    cd ~/.auracoin

    echo ""

    echo "User input is required. Please fill in your account details into the text"
    echo "document that will be opened shortly."
    echo ""
    echo "In order to configure \`outboundIP\`, please write this/these IP address(es)"
    echo "down (the IP address needed should start with 192.168. etc., but there"
    echo "are exceptions):"
    echo ""
    ip -4 addr | grep -oP '(?<=inet\s)\d+(\.\d+){3}'
    echo ""
    echo "If there are port conflicts, feel free to change \`outboundPort\`."
    echo ""
    echo "If you need help, please refer to:"
    echo ""
    echo "https://github.com/auroraenterprise/auracoin/blob/master/docs/download.md#linux-debianubuntu-installation"
    echo ""
    read -p "Press Enter to continue..."

    nano config.auc

    echo ""

    popd &> /dev/null

    echo "Installed successfully!"
    echo "To run Auracoin, navigate to $(pwd) and run \`python3 main.py\`."
    echo "If you wish to have verbose mode, use the \`-v\` parameter."
    echo ""
    read -p "Would you like to run the Auracoin miner now (verbose mode)? [Y/n]" -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pushd . &> /dev/null

        cd auracoin

        python3 main.py -v

        popd &> /dev/null

        echo ""
        echo "Thanks for playing! Have a nice day!"
    else
        echo "All installed. Have a nice day!"
    fi
else 
    echo "Installation cancelled. Have a nice day!"
fi