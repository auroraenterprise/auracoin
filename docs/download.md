# Download Auracoin
Thanks for your interest in Auracoin! Here's how to download the miner.

## First steps
To download the source, please go to [our GitHub repository](https://github.com/auroraenterprise/auracoin) and press the 'Clone or download' button.
If you have Git installed, feel free to
`git clone https://github.com/auroraenterprise/auracoin.git`. If not, just
download the ZIP file and extract it to a sensible place. (You can even rename
the `auracoin-master` folder to whatever you'd like!)

Now at this point, instructions vary by platform. Please read the respective
instructions below!

## Windows installation
First off, make sure that you have administrator privileges to your user folder!

Make sure that you have [Python 3](https://www.python.org/downloads/) downloaded and installed.

Open Command Prompt by searching it in the Start menu. Once it's opened,
navigate to the Auracoin folder, for example with the command
`cd C:\Users\Me\Documents\Auracoin`.

In Command Prompt, type `py -m pip install ecdsa` (if that fails, try running
`py -m pip install ecdsa --user`). `ecdsa` is a library that is needed in order
to process Auracoin transactions.

Again, in Command Prompt, type `py main.py -v`. This will run the Auracoin miner
in verbose mode. You may get a message like
`Your configuration file at ~/.auracoin/config.auc is missing or not configured properly.`.
This is fine as that's what we're gonna be setting up next!

> **Note:** if you get a message after that that says
> `Automatic creation failed, please create the file and any other needed files.`,
> you may need to create the configuration folder and file manually:
>
> In a new Command Prompt window, type `cd %userprofile%` then
> `mkdir .auracoin`. Go to Windows Explorer and navigate to `%userprofile%`
> (type it into the Address Bar). Then go into the `.auracoin` folder.
> Copy the files in the `config` folder from the repository download into the
> `.auracoin` folder (but don't copy the `config` folder itself!).

In Windows Explorer, navigate to `%userprofile%\.auracoin` (type it into the
Address Bar). Open up the `config.auc` file using your favourite text editor
(or Notepad), and enter your account details in order to gain rewards for your
transactions!

> **Note:** Unless you're testing Auracoin locally and not willing to help mine
> Auracoin on the main network, you'll need to set up port forwarding for your
> device. Instructions for routers may vary, but the gist is that you need to
> log into your network router's settings page in order to set it up.

To make sure that your node is connected to the network properly, you'll need to
configure the IP address settings in `config.auc`. To do this, open Command
Prompt and type `ipconfig`. Find your IP under `IPv4 Address` for your adapter
(for example your adapter may be called `Ethernet adapter Ethernet`).

With that IP address (should be starting with `192.168.` etc., but there are
exceptions), enter it into the `outboundIP` property under the `Peers` section
of `config.auc`.

You can change the port that Auracoin runs on by changing `outboundPort` in
`config.auc`.

When you need to run the miner, navigate to the folder containing your Auracoin
repository download and open `main.py`. Alternatively, you could type
`py main.py` in Command Prompt in the respective directory, or if you want it
to run verbosely, just add a `-v` on the end of the command.

## Mac installation
Make sure that you have [Python 3](https://www.python.org/downloads/) downloaded and installed.

Open Terminal by searching it in Spotlight and navigate to the Auracoin folder,
for example with `cd /Users/Me/Documents/Auracoin`.

In Terminal, type `python3 -m pip install ecdsa` (if that fails, try running
`python3 -m pip install ecdsa --user`). `ecdsa` is a library that is needed in
order to process Auracoin transactions.

Again, in Terminal, type `python3 main.py -v`. This will run the Auracoin miner
in verbose mode. You may get a message like
`Your configuration file at ~/.auracoin/config.auc is missing or not configured properly.`.
This is fine as that's what we're gonna be setting up next!

> **Note:** if you get a message after that that says
> `Automatic creation failed, please create the file and any other needed files.`,
> you may need to create the configuration folder and file manually:
>
> In a new Terminal window, type `cd ~` then `mkdir .auracoin`. Go to Finder and
> navigate to your user folder (up from Documents) and then to `.auracoin`.
> Copy the files in the `config` folder from the repository download into the
> `.auracoin` folder (but don't copy the `config` folder itself!).

In Finder, navigate to `~/.auracoin` (up from Documents, then into the
`.auracoin` folder). Open up the `config.auc` file using your favourite text
editor (or TextEdit), and enter your account details in order to gain rewards
for your transactions!

> **Note:** Unless you're testing Auracoin locally and not willing to help mine
> Auracoin on the main network, you'll need to set up port forwarding for your
> device. Instructions for routers may vary, but the gist is that you need to
> log into your network router's settings page in order to set it up.

To make sure that your node is connected to the network properly, you'll need to
configure the IP address settings in `config.auc`. To do this, open Terminal and
type `ifconfig`. Find your IPv4 address for your adapter.

With that IP address (should be starting with `192.168.` etc., but there are
exceptions), enter it into the `outboundIP` property under the `Peers` section
of `config.auc`.

You can change the port that Auracoin runs on by changing `outboundPort` in
`config.auc`.

When you need to run the miner, navigate to the folder containing your Auracoin
repository download and open `main.py`. Alternatively, you could type
`python3 main.py` in Terminal in the respective directory, or if you want it
to run verbosely, just add a `-v` on the end of the command.

## Linux (Debian/Ubuntu) installation
**Good news!** You can easily install Auracoin with this Bash one-liner:

```bash
wget https://aur.xyz/auracoin/get.sh && bash get.sh && rm get.sh
```

You will be easily guided step-by-step as to how to install Auracoin. It cuts
out all of the mundane tasks and allows you to have a rest from the command
line! 😀

If you already have some of the requirements listed below, the script will skip
over installing those requirements, which saves time.

The script is still in beta, so please report any bugs by opening up a new issue
on this repo.

### Alternative/manual method
Make sure that you have [Python 3](https://www.python.org/downloads/) downloaded and installed.
Because it's Linux, you probably already have it installed!

Open your terminal application and navigate to the Auracoin folder, for example
with `cd /home/me/Documents/Auracoin`.

In your terminal, type `python3 -m pip install ecdsa` (if that fails, try
running `python3 -m pip install ecdsa --user`). `ecdsa` is a library that is
needed in order to process Auracoin transactions.

Again, in your terminal, type `python3 main.py -v`. This will run the Auracoin
miner in verbose mode. You may get a message like
`Your configuration file at ~/.auracoin/config.auc is missing or not configured properly.`.
This is fine as that's what we're gonna be setting up next!

> **Note:** if you get a message after that that says
> `Automatic creation failed, please create the file and any other needed files.`,
> you may need to create the configuration folder and file manually:
>
> In a new terminal window, type `cd ~` then `mkdir .auracoin`. Go to your file
> manager and navigate to your user folder (up from Documents) and then to
> `.auracoin`. Copy the files in the `config` folder from the repository
> download into the `.auracoin` folder (but don't copy the `config` folder
itself!).

In your file manager, navigate to `~/.auracoin` (up from Documents, then into
the `.auracoin` folder). Open up the `config.auc` file using your favourite text
editor, and enter your account details in order to gain rewards for your
transactions!

> **Note:** Unless you're testing Auracoin locally and not willing to help mine
> Auracoin on the main network, you'll need to set up port forwarding for your
> device. Instructions for routers may vary, but the gist is that you need to
> log into your network router's settings page in order to set it up.

To make sure that your node is connected to the network properly, you'll need to
configure the IP address settings in `config.auc`. To do this, open your
terminal and type `ifconfig`. Find your IPv4 address for your adapter.

With that IP address (should be starting with `192.168.` etc., but there are
exceptions), enter it into the `outboundIP` property under the `Peers` section
of `config.auc`.

You can change the port that Auracoin runs on by changing `outboundPort` in
`config.auc`.

When you need to run the miner, navigate to the folder containing your Auracoin
repository download and open `main.py`. Alternatively, you could type
`python3 main.py` in a terminal in the respective directory, or if you want it
to run verbosely, just add a `-v` on the end of the command.

## Platform not mentioned here?
If you use a platform that is not mentioned here, feel free to experiment with
downloading Auracoin to run it on your platform!

You can then submit an issue to our repository to tell us to add the platform to
the list.

Suggestions are welcome!