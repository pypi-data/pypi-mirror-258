/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./src/python-kernel/web-worker.js":
/*!*****************************************!*\
  !*** ./src/python-kernel/web-worker.js ***!
  \*****************************************/
/***/ (() => {

eval("if( 'undefined' === typeof window){\r\n    importScripts(\"https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js\");\r\n} \r\n\r\nvar pyodide = null;\r\n\r\nconst reactPyModule = {\r\n    getInput: (prompt) => {\r\n        const request = new XMLHttpRequest()\r\n        request.open('GET', `/py-get-input/?prompt=${prompt}`, false)\r\n        request.send(null)\r\n        return request.responseText\r\n    }\r\n}\r\n\r\nself.onmessage = async function (event) {\r\n    if(event.data.type === \"LOAD_PYODIDE\"){\r\n        setupPromise = setupPyodide();\r\n        await setupPromise;\r\n    }\r\n    if (event.data.type === \"INSTALL\") {\r\n        if (setupPromise) {\r\n            await setupPromise;\r\n        }\r\n        await install_package(event.data.packages);\r\n        self.postMessage({ type: \"PACKAGES_INSTALLED\" });\r\n    }\r\n    if(event.data.type === \"INIT_DB\"){\r\n        let databaseInitQuery = event.data.databaseInitQuery;\r\n        let names = event.data.databaseInitQuery.map((x) => x['name']);\r\n        let queries = event.data.databaseInitQuery.map((x) => x['databaseInitQuery']);\r\n\r\n        const sqliteEasyPackage =  fetch(\"bc_html/_static/sqlite_easy.zip\").then((x) => x.arrayBuffer());;\r\n        const pkg = await sqliteEasyPackage;\r\n        await pyodide.unpackArchive(pkg, \"zip\");\r\n\r\n        await pyodide.loadPackage(['sqlite3'])\r\n        pyodide.runPython(pythonInitCode);\r\n\r\n        for (let i = 0; i < databaseInitQuery.length; i++){\r\n            pyodide.runPython(pythonCreateDatabaseCode(names[i], queries[i]));\r\n        }\r\n        self.postMessage({ type: \"DB_INITIALIZED\" });\r\n    }\r\n    if (event.data.type === \"SET_INTERRUPT_BUFFER\"){\r\n        pyodide.setInterruptBuffer(event.data.interruptBuffer);\r\n    }\r\n    if (event.data.type === \"RUN\") {\r\n            exitCode = await pyodide.runPythonAsync(`run_code('''${event.data.code}''')`)\r\n            if (exitCode === -1) {\r\n                self.postMessage({ type: \"ERR\" });\r\n            }\r\n            self.postMessage({ type: \"CODE_EXECUTED\" });\r\n    }\r\n    if (event.data.type === \"RUN_SQL\") {\r\n        let queryWrapper = event.data.queryWrapper;\r\n        let result = pyodide.runPython(queryWrapper);\r\n        if (result.get('error')) {\r\n            self.postMessage({ type: \"SQL_ERR\", err: result.get('error') });\r\n        }\r\n        else{\r\n            self.postMessage({ type: \"SQL_CODE_EXECUTED\", result: result });\r\n        }\r\n    }\r\n}\r\n\r\nasync function install_package(packages) {\r\n    const micropip = pyodide.pyimport('micropip')\r\n    packages.forEach(async (p) => {\r\n        await micropip.install(p)\r\n    });\r\n}\r\n\r\nasync function setupPyodide() {\r\n    pyodide = await self.loadPyodide({\r\n        stdout: (text) => {\r\n            self.postMessage({ type: \"STDOUT\", text: text })\r\n        },\r\n        stderr: (text) => {\r\n            self.postMessage({ type: \"STDERR\", text: text })\r\n        }\r\n    });\r\n    await pyodide.loadPackage(['pyodide-http'])\r\n    await pyodide.loadPackage(['micropip'])\r\n    pyodide.registerJsModule('react_py', reactPyModule)\r\n\r\n    const initCode = `\r\nimport pyodide_http\r\npyodide_http.patch_all()\r\n`\r\n    await pyodide.runPythonAsync(initCode)\r\n    \r\n    const patchInputCode = `\r\nimport sys, builtins\r\nimport react_py\r\n__prompt_str__ = \"\"\r\ndef get_input(prompt=\"\"):\r\n    global __prompt_str__\r\n    __prompt_str__ = prompt\r\n    print(prompt)\r\n    s = react_py.getInput(prompt)\r\n    print(s)\r\n    return s\r\nbuiltins.input = get_input\r\nsys.stdin.readline = lambda: react_py.getInput( __prompt_str__)\r\n`\r\n    await pyodide.runPythonAsync(patchInputCode)\r\n\r\n    const patchOutputCode = `\r\nimport sys, io, traceback\r\ndef run_code(code):\r\n  try:\r\n      exec(code, {})\r\n      return 0\r\n  except:\r\n      tb = traceback.format_exc().split(\"\\\\n\")\r\n      tb = tb[:1] + tb[2:] # Remove run_code from traceback\r\n      print(\"\\\\n\".join(tb))\r\n      return -1\r\n`\r\n    await pyodide.runPythonAsync(patchOutputCode);\r\n    \r\n    self.postMessage({ type: \"PYODIDE_READY\" });\r\n}\r\n\r\n\r\n//SQLITE EAST WRAPPERS\r\n\r\nconst pythonInitCode = `from sqlite_easy import *\r\ndata_base_connections = {}`;\r\nconst pythonCreateDatabaseCode = (name, query) => `data_base_connections['''${name}'''] = create_database('''${name}''', '''${query}''')`;\n\n//# sourceURL=webpack://plct-web-components/./src/python-kernel/web-worker.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./src/python-kernel/web-worker.js"]();
/******/ 	
/******/ })()
;