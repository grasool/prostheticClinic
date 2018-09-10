from FeatureExtraction import FeatureExtraction as featExt


def testRunFeatExt(tempData):
    fe = featExt()

    rms = fe.extractRMS(tempData)
    print("Root Means Squared (RMS): \n")
    print(rms)
    print("\n--------")


    iav = fe.extractIAV(tempData)
    print("Integraged Absolute Mean (IAV): \n")
    print(iav)
    print("\n--------")

    mav = fe.extractMAV(tempData)
    print("Mean Absolute Value (MAV): \n")
    print(mav)
    print("\n--------")

    mav1 = fe.extractMAV1(tempData)
    print("Meav Absolute Value Type 1 (MAV1)\n")
    print(mav1)
    print("\n--------")

    mav2 = fe.extractMAV2(tempData)
    print("Meav Absolute Value Type 2 (MAV2)\n")
    print(mav2)
    print("\n--------")

    ssi = fe.extractSSI(tempData)
    print("Simple Square Integral (SSI) \n")
    print(ssi)
    print("\n--------")

    var = fe.extractVariance(tempData)
    print("Variance: \n")
    print(var)
    print("\n--------")

    tm3 = fe.extractTM3(tempData)
    print("Temporal Movements 3 \n")
    print(tm3)
    print("\n--------")

    tm4 = fe.extractTM4(tempData)
    print("Temporal Movements 4 \n")
    print(tm4)
    print("\n--------")

    tm5 = fe.extractTM5(tempData)
    print("Temporal Movements 5 \n")
    print(tm5)
    print("\n--------")

    vOrder = fe.extractVOrder(tempData, order = 2)
    print("V Order: \n")
    print(vOrder)
    print("\n--------")

    waveformLength = fe.extractWL(tempData)
    print("Waveform Length (WL):\n")
    print(waveformLength)
    print("\n--------")

    aac = fe.extractAAC(tempData)
    print("Average Amplitude Change (AAC): \n")
    print(aac)
    print("\n--------")

    dasdv = fe.extractDASDV(tempData)
    print("Difference Absolute Standard Deviation Value: \n")
    print(dasdv)
    print("\n--------")


