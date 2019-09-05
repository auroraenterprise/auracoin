# Contribute to Auracoin
Contributions to Auracoin are most welcome! If you're a developer, feel free to
contribute to [our GitHub repository](https://github.com/auroraenterprise/auracoin).

If there are any issues, feel free to submit them! Our developers are happy to
help with the rectification of problems.

Coded a cool new thing that works with Auracoin? Nice! **Make sure that you test
Auracoin on your network by following the steps listed below.** Then, make a
pull request so that we can check, approve and merge your code!

## Testing Auracoin code changes
When testing, please make sure that you only test your changes on your LAN
network using your devices. To create your own genesis block for testing, run
`init.py` and follow the instructions. It may take some time to mine the genesis
block.

Also, make sure that your configuration file's `peerList` doesn't contain main
nodes, or your test blockchain may be overwritten!
