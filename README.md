# ⏳ KronOTP

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Node.js](https://img.shields.io/badge/Node.js-Ready-success)
![Python](https://img.shields.io/badge/Python-Ready-success)

**KronOTP** is a universal, multi-language TOTP (Time-based One-Time Password) engine. Built with a monorepo architecture, it provides native, production-ready modules for generating and verifying 2FA codes across different programming languages.

Whether you are bypassing 2FA in automated testing (Playwright, Puppeteer, Selenium) or building a custom authenticator backend, KronOTP offers a unified, zero-conflict, and highly optimized toolkit.

## 🚀 Available Modules

Each language has its own isolated environment and package manager configuration. Click on the language to view its specific documentation:

* 🟢 **[Node.js / JavaScript](./javascript)** — Publishable to `npm`
* 🔵 **[Python](./python)** — Publishable to `PyPI`
* 🟡 **[Go](./go)** — *Coming Soon*
* 🟣 **[PHP](./php)** — *Coming Soon*

## 💡 Why KronOTP?

- **Automation First:** Perfectly designed for headless browsers and CI/CD testing pipelines.
- **Cross-Platform Consistency:** Get the exact same functionality and structure regardless of the language you code in.
- **RFC 6238 Compliant:** Strictly follows standard TOTP algorithm guidelines.
- **Zero Conflicts:** Isolated sub-directories ensure `npm`, `pip`, and other package managers never interfere with each other.

## 📁 Monorepo Structure

```text
KronOTP/
├── javascript/        # npm package (totp generator for JS environments)
├── python/            # PyPI package (totp generator for Python environments)
├── go/                # Future Go implementation
├── README.md          # You are here
└── LICENSE            # MIT License
```

## ⚡ Quick Preview

**Using Node.js:**
```javascript
const KronOTP = require('./javascript/src/kron-otp');
const code = KronOTP.generate('JBSWY3DPEHPK3PXP');
console.log('2FA Code:', code);
```

**Using Python:**
```python
from python.src.kron_otp import KronOTP
code = KronOTP.generate('JBSWY3DPEHPK3PXP')
print(f"2FA Code: {code}")
```

## 🤝 Contributing
Contributions are always welcome! Feel free to open an issue or submit a pull request if you want to add support for a new language.

## 📝 License
This project is licensed under the [MIT License](LICENSE).