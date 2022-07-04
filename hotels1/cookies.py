import requests
from requests import session
import json
from pprint import pprint
from urllib import request

#headers = {
#    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
#    "Cookie" : "PL_CINFO=029b7d69b722ee5968c940730d841da1~1635348836~v2; SITESERVER=ID=029b7d69b722ee5968c940730d841da1; _pxhd=SIOHAJTM5GJYCCT06OIH8YznnqkXX5fd5LPsoqK6e3KTgCat9t-2NL12VJVrNSXU1uCUTGBTIE5DtPsiRefSoA==:ap-fIEdYTpqUimxMnZYSbc7PNmAJ3Teq-ftvBapuDw-7RoCDy9P2KdYuu-b-8L9VXwBmaMpTmxjh2loToN3tRIxmrugcrN8vDbaJO-ST2XA=",
#    "Accept": "*/*",
#    "Accept-Encoding": "gzip, deflate, br",
#    "Accept-Language": "en-US,en;q=0.9,bn;q=0.8,es;q=0.7,ar;q=0.6",
#    "Connection": "keep-alive",
#    #"Content-Length": "1843",
#    "Content-Type": "application/json",
#    'origin': 'https://www.priceline.com',
#    'referer': 'https://www.priceline.com/relax/at/478502/from/20220523/to/20220527/rooms/1/adults/2?vrid=2af9fb11ff31fc1a4170ac6a891116da',
#
#
#}

headers = {
            'accept':'*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,bn;q=0.8,es;q=0.7,ar;q=0.6',
            'apollographql-client-name': 'relax',
            'apollographql-client-version': 'master-1.1.813',
            'content-length': '3453',
            'content-type': 'application/json',
            'origin': 'https://www.priceline.com',
            'referer': 'https://www.priceline.com/relax/at/478502/from/20220523/to/20220527/rooms/1/adults/2?vrid=bd9ebbc30ca405d48687eddb2e9ff1bb',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
                }


payload2 = {"query":"query getHotelDetails($hotelID: ID, $allInclusive: Boolean, $checkIn: String, $checkOut: String, $roomsCount: Int, $cguid: ID, $cugdor: String, $currencyCode: String, $pclnID: ID, $metaID: ID, $metaHotelId: ID, $rehabRateKey: ID, $preferredRateID: ID, $rID: ID, $rateDisplayOption: String, $rguid: ID, $visitId: String, $refClickID: String, $reviewCount: Float, $paymentRateMerge: Boolean, $multiOccDisplay: Boolean, $multiOccRates: Boolean, $appCode: String, $adults: Int, $children: [String], $unlockDeals: Boolean, $authToken: ID, $responseOptions: String, $includePrepaidFeeRates: Boolean, $addErrToResponse: Boolean, $packagesDetailsSearchQuery: HotelPsapiDetailsArguments) {\n  details: hotelDetails(hotelID: $hotelID, checkIn: $checkIn, checkOut: $checkOut, roomsCount: $roomsCount, cguid: $cguid, cugdor: $cugdor, currencyCode: $currencyCode, pclnID: $pclnID, metaID: $metaID, metaHotelId: $metaHotelId, rehabRateKey: $rehabRateKey, preferredRateID: $preferredRateID, rID: $rID, rateDisplayOption: $rateDisplayOption, rguid: $rguid, visitId: $visitId, refClickID: $refClickID, reviewCount: $reviewCount, paymentRateMerge: $paymentRateMerge, multiOccDisplay: $multiOccDisplay, multiOccRates: $multiOccRates, appCode: $appCode, adults: $adults, children: $children, allInclusive: $allInclusive, unlockDeals: $unlockDeals, authToken: $authToken, responseOptions: $responseOptions, includePrepaidFeeRates: $includePrepaidFeeRates, addErrToResponse: $addErrToResponse, packagesDetailsSearchQuery: $packagesDetailsSearchQuery) {\n    rguid\n    errorMessage\n    hotel {\n      pkgComponentIndex\n      maxPricedOccupancy\n      maxOccupancy\n      merchandisingInfo {\n        color\n        badgeText\n        bannerHeader\n        bannerText\n        __typename\n      }\n      reasonsToBook {\n        color\n        icon\n        header\n        substring\n        __typename\n      }\n      hotelViewCount {\n        cumulativeViewCount\n        __typename\n      }\n      commonRoomAmenities {\n        type\n        name\n        __typename\n      }\n      recmdScore\n      totalReviewCount\n      overallGuestRating\n      rooms {\n        isUnlockedMemberDeal\n        displayableRates {\n          originalRates {\n            gid\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      transformedRooms {\n        maxPricedOccupancy\n        roomDisplayName\n        maxOccupancy\n        isGreatForFamily\n        roomId\n        longDescription\n        roomFacilities\n        cleanliness {\n          score\n          totalReviews\n          __typename\n        }\n        beddingOption\n        bedCount\n        roomThumbnailUrl\n        roomSize\n        amenities {\n          code\n          __typename\n        }\n        imageUrls {\n          largeUrl\n          mediumUrl\n          __typename\n        }\n        roomOccupancies {\n          roomCode\n          numberOfAdults\n          numberOfChildren\n          numberOfBeds\n          numberOfRooms\n          __typename\n        }\n        roomRates {\n          cartToken\n          pkgPriceInformation {\n            totalCost\n            totalCostPerTraveler\n            totalCostWithHotelMandatoryFees\n            totalPayNow\n            totalPayLater\n            totalSavings\n            originalCostPerTraveler\n            totalStrikethrough\n            totalHotelMandatoryFees\n            roomMandatoryFees\n            __typename\n          }\n          preferredRateFlag\n          pricedOccupancy\n          couponApplicable\n          suggestedNumOfRooms\n          mergedRate {\n            isFullyUnlocked\n            rateIdentifier\n            price\n            grandTotal\n            currencySymbol\n            roomsLeft\n            cancellationPolicy\n            cancellationPolicyLongText\n            cancellationMsg\n            refundPolicy\n            debugString\n            paymentOptionsText\n            feeAmount\n            isPayLater\n            isUniversalCartEligible\n            isXSellEligible\n            __typename\n          }\n          isPayLater\n          rateIdentifier\n          isBestDeal\n          price\n          grandTotal\n          currencySymbol\n          roomsLeft\n          strikeThroughPrice\n          isFreeCancellation\n          cancellationPolicy\n          cancellationPolicyLongText\n          cancellationMsg\n          ccRequired\n          refundPolicy\n          savingPct\n          payLaterMessage\n          feeAmount\n          bannerText\n          programName\n          merchandisingFlag\n          rateLevelAmenities {\n            name\n            isHighlighted\n            __typename\n          }\n          totalPriceExcludingTaxesAndFeePerStay\n          paymentOptionsText\n          disclaimerMessage\n          debugString\n          promos {\n            promoType\n            isVariableMarkupPromo\n            title\n            desc\n            isHighlighted\n            __typename\n          }\n          isFullyUnlocked\n          incrementalPricingIconName\n          isUniversalCartEligible\n          basketPriceKey\n          isXSellEligible\n          itemDetailsKey\n          bundlePriceKey\n          rateKey\n          __typename\n        }\n        cartToken\n        basketPriceKey\n        itemDetailsKey\n        priceKey\n        bundlePriceKey\n        token\n        planCode\n        rateTypeCode\n        gdsName\n        __typename\n      }\n      guestReviews {\n        firstName\n        overallScore\n        reviewTextGeneral\n        reviewTextNegative\n        reviewTextPositive\n        sourceCode\n        travelerType\n        travelerTypeId\n        creationDate\n        __typename\n      }\n      reviewRatingSummary {\n        ratings {\n          description\n          label\n          score\n          summaryCount\n          summaryValue\n          __typename\n        }\n        travelerType {\n          count\n          id\n          type\n          __typename\n        }\n        __typename\n      }\n      signInDealsAvailable\n      signInDealsMinRate\n      ratings {\n        category\n        score\n        __typename\n      }\n      bookings {\n        firstName\n        lastNameInitial\n        bookedPrice\n        bookedCurrencyCode\n        justBookedBadge\n        __typename\n      }\n      ratesSummary {\n        pricedOccupancy\n        suggestedNumOfRooms\n        freeCancelableRateAvail\n        minPrice\n        totalCostPerTraveler\n        minStrikePrice\n        promptUserToNativeApp\n        savingsClaimStrikePrice\n        savingsClaimDisclaimer\n        savingsClaimPercentage\n        minCurrencyCodeSymbol\n        minCurrencyCode\n        roomLeft\n        payWhenYouStayAvailable\n        pclnId\n        programName\n        merchandisingFlag\n        preferredRateId\n        rateIdentifier\n        showRecommendation\n        suggestedNumOfRooms\n        status\n        __typename\n      }\n      hasNodateRooms\n      isAllInclusiveHotel\n      location {\n        neighborhoodDescription\n        __typename\n      }\n      hotelFeatures {\n        features\n        highlightedAmenities\n        hotelAmenities {\n          code\n          displayable\n          free\n          name\n          type\n          __typename\n        }\n        topAmenities\n        breakfastDetails\n        __typename\n      }\n      policies {\n        checkInTime\n        checkOutTime\n        petDescription\n        childrenDescription\n        importantInfo\n        __typename\n      }\n      itemKey\n      basketItemKey\n      componentKey\n      retailPrice {\n        pricePerPerson\n        displayPricePerPerson\n        amount\n        displayAmount\n        __typename\n      }\n      images {\n        imageHDURL\n        imageURL\n        __typename\n      }\n      __typename\n    }\n    componentKeyMap\n    los\n    signInDealRelatedInfo {\n      promptUserToSignIn\n      __typename\n    }\n    __typename\n  }\n}\n","variables":{"appCode":"DESKTOP","cguid":"b6a02daf29ebfcd2d3a1f83498e688da","checkIn":"20220523","checkOut":"20220527","rID":"DTDIRECT","roomsCount":1,"currencyCode":"USD","refClickID":"","unlockDeals":True,"includePrepaidFeeRates":True,"visitId":"20211028160655190c1a0d-RRLXGQD","addErrToResponse":True,"adults":2,"paymentRateMerge":False,"multiOccDisplay":True,"multiOccRates":True,"hotelID":"478502","rateDisplayOption":"S","reviewCount":5,"responseOptions":"POP_COUNT,REVIEWS,CUSTOM_DESC,RATE_SUMMARY,RATINGS,DETAILED_ROOM,HOTEL_IMAGES,RATE_IMPORTANT_INFO,RATE_CHARGES_DETAIL,PROXIMITY,BOOKINGS,NORATEROOMS,REFUND_INFO"},"operationName":"getHotelDetails"}
url = "https://www.priceline.com/pws/v0/pcln-graph/"

s = requests.session()

r = s.post(url,  data = json.dumps(payload2), headers = headers)

print(r.cookies.get_dict())

data = r.json()
data = data['data']['details']

data = data['hotel']

data = data['ratesSummary']

features = {
     'Price' : data['minPrice'],
     'Status' : data['status']
}

print(features)

hotel_id2 = payload2['variables']['hotelID']
print(hotel_id2)
