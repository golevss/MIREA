defineRule("lamp_control",{
    whenChanged: "wb-mdm3_57/Channel 1",
        then : function (newValue, devName, cellName){
            if (newValue > 50){
                dev["buzzer" ] ["enable"] = true;
            }else{
                dev["buzzer"]["enable"] = false;
            }
            dev["buzzer"]["frequency"] = newValue;
        }
});
