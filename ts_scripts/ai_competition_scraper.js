"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
var axios_1 = require("axios");
var cheerio = require("cheerio");
var fs = require("fs");
function scrapeAICompetition() {
    return __awaiter(this, void 0, void 0, function () {
        var companies, results, _i, companies_1, company, url, response, $, latestVersion, error_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    companies = ["OpenAI", "xAI", "Gemini", "Anthropic"];
                    results = {};
                    _i = 0, companies_1 = companies;
                    _a.label = 1;
                case 1:
                    if (!(_i < companies_1.length)) return [3 /*break*/, 6];
                    company = companies_1[_i];
                    url = "https://www.google.com/search?q=".concat(company, "+latest+LLM+version");
                    _a.label = 2;
                case 2:
                    _a.trys.push([2, 4, , 5]);
                    return [4 /*yield*/, axios_1.default.get(url)];
                case 3:
                    response = _a.sent();
                    $ = cheerio.load(response.data);
                    latestVersion = $('.BNeawe').first().text() || 'Not found';
                    results[company] = latestVersion;
                    return [3 /*break*/, 5];
                case 4:
                    error_1 = _a.sent();
                    console.error("Error fetching data for ".concat(company, ":"), error_1);
                    results[company] = 'Error';
                    return [3 /*break*/, 5];
                case 5:
                    _i++;
                    return [3 /*break*/, 1];
                case 6: return [2 /*return*/, results];
            }
        });
    });
}
function main() {
    return __awaiter(this, void 0, void 0, function () {
        var data, report;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, scrapeAICompetition()];
                case 1:
                    data = _a.sent();
                    report = "# AI Competition Report\n\n" +
                        Object.entries(data).map(function (_a) {
                            var company = _a[0], version = _a[1];
                            return "## ".concat(company, "\nLatest LLM Version: ").concat(version, "\n\n");
                        }).join('');
                    fs.writeFileSync('report.md', report, 'utf-8');
                    return [2 /*return*/];
            }
        });
    });
}
main().catch(console.error);
