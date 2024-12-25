# StayUp 🖱️

[![PyPI version](https://badge.fury.io/py/stayup.svg)](https://badge.fury.io/py/stayup)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/stayup.svg)](https://pypi.org/project/stayup/)

A modern Python package to prevent system sleep by simulating small mouse movements. Perfect for keeping your system awake during long downloads, installations, or when you need to maintain an active system state. 💻✨

## ✨ Features

- 🎯 Configurable mouse movement intervals
- ⏱️ Adjustable movement duration and distance
- ⌛ Run for a specific duration or until a command completes
- 🛡️ Safe movement patterns that avoid screen edges
- 🛑 Graceful shutdown with Ctrl+C
- 🔇 Quiet mode for reduced output

## 🚀 Installation

```bash
pip install stayup
```

## 📖 Usage

### Basic Usage

```bash
# Run with default settings (moves mouse every 5 minutes)
stayup

# Run for 2 hours
stayup --run-for 120

# Run until a specific command completes
stayup --wait-cmd "pip install large-package"

# Move mouse every 2 minutes with 0.2s movement duration
stayup --interval 120 --duration-movement 0.2
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--run-for` | Run for specified number of minutes | - |
| `--wait-cmd` | Run until the specified command completes | - |
| `--interval` | Interval between mouse movements in seconds | 60 |
| `--duration-movement` | Duration of mouse movement in seconds | 0.1 |
| `--movement-distance` | Distance in pixels for mouse movement | 1 |
| `--disable-failsafe` | Disable the failsafe feature | False |
| `--quiet` | Reduce output verbosity | False |

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for how to get started.

## 🐛 Bug Reports & Feature Requests

If you encounter any bugs or have ideas for new features, please open an issue on our [GitHub Issues](https://github.com/manthanmtg/stayup/issues) page.

## 📜 License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the [LICENSE](LICENSE) file for details.

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=manthanmtg/stayup&type=Date)](https://star-history.com/#manthanmtg/stayup&Date)

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/manthanmtg/stayup?style=social)
![GitHub forks](https://img.shields.io/github/forks/manthanmtg/stayup?style=social)

---
Made with ❤️ by the StayUp team