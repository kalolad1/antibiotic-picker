module.exports = {
    "env": {
        "browser": true,
        "es2021": true
    },
    "extends": [
        "standard-with-typescript",
        "plugin:react/recommended"
    ],
    "overrides": [
        {
            "env": {
                "node": true
            },
            "files": [
                ".eslintrc.{js,cjs}"
            ],
            "parserOptions": {
                "sourceType": "script"
            }
        }
    ],
    "parserOptions": {
        "ecmaVersion": "latest",
        "sourceType": "module"
    },
    "plugins": [
        "react"
    ],
    "rules": {
        // suppress errors for missing 'import React' in files
        "react/react-in-jsx-scope": "off",
        "@typescript-eslint/consistent-type-assertions": "off",
        "@typescript-eslint/no-non-null-assertion": "off",
        "react/no-children-prop": "off"
    }
}
