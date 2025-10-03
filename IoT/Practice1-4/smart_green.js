defineRule("lamp_control", {
    whenChanged: "wb-msw-v4 64/Temperature",
        then : function (newValue, devName, cellName){
            if (newValue < 25){
                dev["wb-mdm3_57"]["Channel 1"] = 100;
                dev["wb-mdm3_57"]["Input 1"] = true;
                dev["wb-led_39"]["RGB Palette"] = {"r":255,"g":255,"b":0};
                dev["wb-led_39"]["RGB Strip"] = true;
            }else{
                dev["wb-mdm3_57"]["Channel 1"] = 0;
                dev["wb-mdm3_57"]["Input 1"] = false;
                dev["wb-led_39"]["RGB Palette"] = {"r":0,"g":0,"b":0};
                dev["wwb-led_39"]["RGB Strip"] = false;
            }}
});
