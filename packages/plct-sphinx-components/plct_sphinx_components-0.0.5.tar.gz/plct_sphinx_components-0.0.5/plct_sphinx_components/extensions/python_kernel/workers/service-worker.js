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

/***/ "./src/python-kernel/service-worker.js":
/*!*********************************************!*\
  !*** ./src/python-kernel/service-worker.js ***!
  \*********************************************/
/***/ (() => {

eval("addEventListener('install', () => {\r\n    self.skipWaiting();\r\n});\r\naddEventListener('activate', () => {\r\n    self.clients.claim();\r\n});\r\n\r\nlet resolver = null;\r\n\r\naddEventListener('fetch', (event) => {\r\n    const url = new URL(event.request.url)\r\n\r\n    if (url.pathname.endsWith('/py-get-input/')) {\r\n        const prompt = url.searchParams.get('prompt')\r\n\r\n        event.waitUntil(\r\n            (async () => {\r\n                self.clients.matchAll().then((clients) => {\r\n                    clients.forEach((client) => {\r\n                        if (client.type === 'window') {\r\n                            client.postMessage({\r\n                                type: 'PY_AWAITING_INPUT',\r\n                                prompt\r\n                            })\r\n                        }\r\n                    })\r\n                })\r\n            })()\r\n        )\r\n        const promise = new Promise((r) => {\r\n            resolver = r;\r\n        });\r\n        event.respondWith(promise)\r\n    }\r\n});\r\n\r\naddEventListener('message', (event) => {\r\n    if (event.data.type === 'PY_INPUT') {\r\n        if (!resolver) {\r\n            console.error('Error handing input: No resolver')\r\n            return\r\n        }\r\n        resolver(new Response(event.data.value, { status: 200 }))\r\n        resolver = null; \r\n    }\r\n});\r\n\r\n\n\n//# sourceURL=webpack://plct-web-components/./src/python-kernel/service-worker.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./src/python-kernel/service-worker.js"]();
/******/ 	
/******/ })()
;