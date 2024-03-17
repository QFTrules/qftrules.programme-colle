"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var vscode = require("vscode");
// import * as fs from 'fs';
// import * as path from 'path';
var ProgShow = /** @class */ (function () {
    function ProgShow() {
        this.data = [new TreeItem('cars', [
                new TreeItem('Ford', [new TreeItem('Fiesta'), new TreeItem('Focus'), new TreeItem('Mustang')]),
                new TreeItem('BMW', [new TreeItem('320'), new TreeItem('X3'), new TreeItem('X5')])
            ])];
    }
    ProgShow.prototype.getTreeItem = function (element) {
        return element;
    };
    ProgShow.prototype.getChildren = function (element) {
        if (element === undefined) {
            return this.data;
        }
        return element.children;
    };
    return ProgShow;
}());
var TreeItem = /** @class */ (function (_super) {
    __extends(TreeItem, _super);
    function TreeItem(label, children) {
        var _this = _super.call(this, label, children === undefined ? vscode.TreeItemCollapsibleState.None :
            vscode.TreeItemCollapsibleState.Expanded) || this;
        _this.children = children;
        return _this;
    }
    return TreeItem;
}(vscode.TreeItem));
vscode.window.registerTreeDataProvider('programme-colle', new ProgShow());
