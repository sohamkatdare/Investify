const alphaVantageKeys = ['3KO7PKW2Y0W33Y7U', '5E822IY1ZD9BV9WG', 'Z2PS1DVVXB5LRCOA', '41WURLT2FF7V59NC', 'O8H3J2UJTXM8BOU3', 'BHDXLMDZBOTATM41', '4UARUGMVC3L45I5D', 'LRUYC44GTUE6CQ9W', 'BU9TEKX0HK58A6U4', '4KGSXKQLAUYI8JJI'];
let alphaVantageIndex = 0;

function getAlphaVantageKey() {
    alphaVantageIndex += 1;
    alphaVantageIndex = alphaVantageIndex % alphaVantageKeys.length
    return alphaVantageKeys[alphaVantageIndex]
}