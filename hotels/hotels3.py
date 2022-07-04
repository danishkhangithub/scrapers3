# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import FormRequest
import urllib
import os
import json
import csv
import datetime

# property scraper class
class Hotels(scrapy.Spider):
    # scraper name
    name = 'therapists'
    #start_url = 'https://www.priceline.com/relax/at/478502/from/20220523/to/20220527/rooms/1/adults/2?vrid=2af9fb11ff31fc1a4170ac6a891116da'
    base_url = 'https://www.priceline.com/pws/v0/pcln-graph/'
    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }

    custom_settings = {
       'CONCURRENT_REQUEST_PER_DOMAIN': 6,
       'CONCURRENT_REQUESTS_PER_IP' : 6,
       'DOWNLOAD_DELAY': 10,
       'DOWNLOAD_TIMEOUT' : 10,
       'AUTO_THROTTLE' : False,
        # enable the middleware
       'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 610},

        # enable crawlera
        'CRAWLERA_ENABLED': False,

        # the APIkey you get with your subscription
        'CRAWLERA_APIKEY': '89d13c9b2dd6414aafd11e7952b0769b',

        'CRAWLERA_URL'      : 'http://123compareme.crawlera.com:8010',
        'ROBOTSTXT_OBEY' : 'True'

    }


    headers2 = {
                'accept':' */*',
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

    # payload
    #payload = {"query":"query getHotelContentDeals($deals: [ContentDealType], $cguid: String, $rid: String, $at: String, $rguid: String, $visitId: String, $appc: String, $responseOptions: String, $addErrToResponse: Boolean, $googleMapStatic: GoogleMapStaticArguments) {\n  hotelContent(deals: $deals, rid: $rid, at: $at, rguid: $rguid, cguid: $cguid, visitId: $visitId, appc: $appc, responseOptions: $responseOptions, addErrToResponse: $addErrToResponse, googleMapStatic: $googleMapStatic) {\n    rguid\n    errorMessage\n    hotels {\n      name\n      starRating\n      hotelId\n      pclnId\n      brandId\n      chainCode\n      taxId\n      propertyTypeId\n      quotes {\n        text\n        __typename\n      }\n      childrenStayFree\n      maxChildrenStayFreeAge\n      maxChildrenStayFreeNum\n      customDesc {\n        paragraphTitle\n        text\n        __typename\n      }\n      description\n      hotelThemes {\n        hotelThemeId\n        hotelThemeName\n        __typename\n      }\n      guaranteedBrandsIcon {\n        icon\n        name\n        iconName\n        __typename\n      }\n      policies {\n        additionalPolicies\n        cardsAccepted\n        checkInTime\n        checkOutTime\n        parkingPolicy {\n          policyText\n          freeParking\n          __typename\n        }\n        internetPolicy {\n          policyText\n          freeInternet\n          __typename\n        }\n        childPolicy {\n          policyText\n          childrenStayFree\n          __typename\n        }\n        childrenDescription\n        importantInfo\n        coronaInfoCheck\n        coronaImportantInfo\n        petDescription\n        __typename\n      }\n      location {\n        neighborhoodName\n        neighborhoodDescription\n        neighborhoodId\n        lat\n        lon\n        address {\n          addressLine1\n          cityName\n          provinceCode\n          countryName\n          zip\n          phone\n          isoCountryCode\n          __typename\n        }\n        googleMapStatic {\n          url\n          __typename\n        }\n        cityID\n        zoneId\n        __typename\n      }\n      hotelFeatures {\n        breakfastDetails\n        features\n        topAmenities\n        hotelAmenities {\n          code\n          displayable\n          filterable\n          free\n          name\n          type\n          category\n          categoryId\n          globalAmenityName\n          relatedImages {\n            urls\n            __typename\n          }\n          __typename\n        }\n        cleanlinessAmensList\n        highlightedAmenities\n        amenityCategories {\n          categoryId\n          relatedImages {\n            urls\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      hotelOtherInfo {\n        hotelOtherInfoData {\n          id\n          name\n          detail\n          __typename\n        }\n        __typename\n      }\n      images {\n        imageHDUrl\n        imageUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n","variables":{"deals":[{"dealId": '',"isSopqHotel":False}],"appc":"DESKTOP","rid":"DTDIRECT","responseOptions":"ALL_AMENITIES,HOTEL_IMAGES,UHD_IMAGES","cguid":"b6a02daf29ebfcd2d3a1f83498e688da","visitId":"2021102715122841282f06-RRLXGQD","addErrToResponse":True,"googleMapStatic":{"size":{"x":320}}},"operationName":"getHotelContentDeals"}

    payload = {"query":"query getHotelContentDeals($deals: [ContentDealType], $cguid: String, $rid: String, $at: String, $rguid: String, $visitId: String, $appc: String, $responseOptions: String, $addErrToResponse: Boolean, $googleMapStatic: GoogleMapStaticArguments) {\n  hotelContent(deals: $deals, rid: $rid, at: $at, rguid: $rguid, cguid: $cguid, visitId: $visitId, appc: $appc, responseOptions: $responseOptions, addErrToResponse: $addErrToResponse, googleMapStatic: $googleMapStatic) {\n    rguid\n    errorMessage\n    hotels {\n      name\n      starRating\n      hotelId\n      pclnId\n      brandId\n      chainCode\n      taxId\n      propertyTypeId\n      quotes {\n        text\n        __typename\n      }\n      childrenStayFree\n      maxChildrenStayFreeAge\n      maxChildrenStayFreeNum\n      customDesc {\n        paragraphTitle\n        text\n        __typename\n      }\n      description\n      hotelThemes {\n        hotelThemeId\n        hotelThemeName\n        __typename\n      }\n      guaranteedBrandsIcon {\n        icon\n        name\n        iconName\n        __typename\n      }\n      policies {\n        additionalPolicies\n        cardsAccepted\n        checkInTime\n        checkOutTime\n        parkingPolicy {\n          policyText\n          freeParking\n          __typename\n        }\n        internetPolicy {\n          policyText\n          freeInternet\n          __typename\n        }\n        childPolicy {\n          policyText\n          childrenStayFree\n          __typename\n        }\n        childrenDescription\n        importantInfo\n        coronaInfoCheck\n        coronaImportantInfo\n        petDescription\n        __typename\n      }\n      location {\n        neighborhoodName\n        neighborhoodDescription\n        neighborhoodId\n        lat\n        lon\n        address {\n          addressLine1\n          cityName\n          provinceCode\n          countryName\n          zip\n          phone\n          isoCountryCode\n          __typename\n        }\n        googleMapStatic {\n          url\n          __typename\n        }\n        cityID\n        zoneId\n        __typename\n      }\n      hotelFeatures {\n        breakfastDetails\n        features\n        topAmenities\n        hotelAmenities {\n          code\n          displayable\n          filterable\n          free\n          name\n          type\n          category\n          categoryId\n          globalAmenityName\n          relatedImages {\n            urls\n            __typename\n          }\n          __typename\n        }\n        cleanlinessAmensList\n        highlightedAmenities\n        amenityCategories {\n          categoryId\n          relatedImages {\n            urls\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      hotelOtherInfo {\n        hotelOtherInfoData {\n          id\n          name\n          detail\n          __typename\n        }\n        __typename\n      }\n      images {\n        imageHDUrl\n        imageUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n","variables":{"deals":[{"dealId":"","isSopqHotel":False}],"appc":"DESKTOP","rid":"DTDIRECT","responseOptions":"ALL_AMENITIES,HOTEL_IMAGES,UHD_IMAGES","cguid":"b6a02daf29ebfcd2d3a1f83498e688da","visitId":"202110280935250903aee0-RRLXGQD","addErrToResponse":True,"googleMapStatic":{"size":{"x":320}}},"operationName":"getHotelContentDeals"}

    payload2 = {"query":"query getHotelDetails($hotelID: ID, $allInclusive: Boolean, $checkIn: String, $checkOut: String, $roomsCount: Int, $cguid: ID, $cugdor: String, $currencyCode: String, $pclnID: ID, $metaID: ID, $metaHotelId: ID, $rehabRateKey: ID, $preferredRateID: ID, $rID: ID, $rateDisplayOption: String, $rguid: ID, $visitId: String, $refClickID: String, $reviewCount: Float, $paymentRateMerge: Boolean, $multiOccDisplay: Boolean, $multiOccRates: Boolean, $appCode: String, $adults: Int, $children: [String], $unlockDeals: Boolean, $authToken: ID, $responseOptions: String, $includePrepaidFeeRates: Boolean, $addErrToResponse: Boolean, $packagesDetailsSearchQuery: HotelPsapiDetailsArguments) {\n  details: hotelDetails(hotelID: $hotelID, checkIn: $checkIn, checkOut: $checkOut, roomsCount: $roomsCount, cguid: $cguid, cugdor: $cugdor, currencyCode: $currencyCode, pclnID: $pclnID, metaID: $metaID, metaHotelId: $metaHotelId, rehabRateKey: $rehabRateKey, preferredRateID: $preferredRateID, rID: $rID, rateDisplayOption: $rateDisplayOption, rguid: $rguid, visitId: $visitId, refClickID: $refClickID, reviewCount: $reviewCount, paymentRateMerge: $paymentRateMerge, multiOccDisplay: $multiOccDisplay, multiOccRates: $multiOccRates, appCode: $appCode, adults: $adults, children: $children, allInclusive: $allInclusive, unlockDeals: $unlockDeals, authToken: $authToken, responseOptions: $responseOptions, includePrepaidFeeRates: $includePrepaidFeeRates, addErrToResponse: $addErrToResponse, packagesDetailsSearchQuery: $packagesDetailsSearchQuery) {\n    rguid\n    errorMessage\n    hotel {\n      pkgComponentIndex\n      maxPricedOccupancy\n      maxOccupancy\n      merchandisingInfo {\n        color\n        badgeText\n        bannerHeader\n        bannerText\n        __typename\n      }\n      reasonsToBook {\n        color\n        icon\n        header\n        substring\n        __typename\n      }\n      hotelViewCount {\n        cumulativeViewCount\n        __typename\n      }\n      commonRoomAmenities {\n        type\n        name\n        __typename\n      }\n      recmdScore\n      totalReviewCount\n      overallGuestRating\n      rooms {\n        isUnlockedMemberDeal\n        displayableRates {\n          originalRates {\n            gid\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      transformedRooms {\n        maxPricedOccupancy\n        roomDisplayName\n        maxOccupancy\n        isGreatForFamily\n        roomId\n        longDescription\n        roomFacilities\n        cleanliness {\n          score\n          totalReviews\n          __typename\n        }\n        beddingOption\n        bedCount\n        roomThumbnailUrl\n        roomSize\n        amenities {\n          code\n          __typename\n        }\n        imageUrls {\n          largeUrl\n          mediumUrl\n          __typename\n        }\n        roomOccupancies {\n          roomCode\n          numberOfAdults\n          numberOfChildren\n          numberOfBeds\n          numberOfRooms\n          __typename\n        }\n        roomRates {\n          cartToken\n          pkgPriceInformation {\n            totalCost\n            totalCostPerTraveler\n            totalCostWithHotelMandatoryFees\n            totalPayNow\n            totalPayLater\n            totalSavings\n            originalCostPerTraveler\n            totalStrikethrough\n            totalHotelMandatoryFees\n            roomMandatoryFees\n            __typename\n          }\n          preferredRateFlag\n          pricedOccupancy\n          couponApplicable\n          suggestedNumOfRooms\n          mergedRate {\n            isFullyUnlocked\n            rateIdentifier\n            price\n            grandTotal\n            currencySymbol\n            roomsLeft\n            cancellationPolicy\n            cancellationPolicyLongText\n            cancellationMsg\n            refundPolicy\n            debugString\n            paymentOptionsText\n            feeAmount\n            isPayLater\n            isUniversalCartEligible\n            isXSellEligible\n            __typename\n          }\n          isPayLater\n          rateIdentifier\n          isBestDeal\n          price\n          grandTotal\n          currencySymbol\n          roomsLeft\n          strikeThroughPrice\n          isFreeCancellation\n          cancellationPolicy\n          cancellationPolicyLongText\n          cancellationMsg\n          ccRequired\n          refundPolicy\n          savingPct\n          payLaterMessage\n          feeAmount\n          bannerText\n          programName\n          merchandisingFlag\n          rateLevelAmenities {\n            name\n            isHighlighted\n            __typename\n          }\n          totalPriceExcludingTaxesAndFeePerStay\n          paymentOptionsText\n          disclaimerMessage\n          debugString\n          promos {\n            promoType\n            isVariableMarkupPromo\n            title\n            desc\n            isHighlighted\n            __typename\n          }\n          isFullyUnlocked\n          incrementalPricingIconName\n          isUniversalCartEligible\n          basketPriceKey\n          isXSellEligible\n          itemDetailsKey\n          bundlePriceKey\n          rateKey\n          __typename\n        }\n        cartToken\n        basketPriceKey\n        itemDetailsKey\n        priceKey\n        bundlePriceKey\n        token\n        planCode\n        rateTypeCode\n        gdsName\n        __typename\n      }\n      guestReviews {\n        firstName\n        overallScore\n        reviewTextGeneral\n        reviewTextNegative\n        reviewTextPositive\n        sourceCode\n        travelerType\n        travelerTypeId\n        creationDate\n        __typename\n      }\n      reviewRatingSummary {\n        ratings {\n          description\n          label\n          score\n          summaryCount\n          summaryValue\n          __typename\n        }\n        travelerType {\n          count\n          id\n          type\n          __typename\n        }\n        __typename\n      }\n      signInDealsAvailable\n      signInDealsMinRate\n      ratings {\n        category\n        score\n        __typename\n      }\n      bookings {\n        firstName\n        lastNameInitial\n        bookedPrice\n        bookedCurrencyCode\n        justBookedBadge\n        __typename\n      }\n      ratesSummary {\n        pricedOccupancy\n        suggestedNumOfRooms\n        freeCancelableRateAvail\n        minPrice\n        totalCostPerTraveler\n        minStrikePrice\n        promptUserToNativeApp\n        savingsClaimStrikePrice\n        savingsClaimDisclaimer\n        savingsClaimPercentage\n        minCurrencyCodeSymbol\n        minCurrencyCode\n        roomLeft\n        payWhenYouStayAvailable\n        pclnId\n        programName\n        merchandisingFlag\n        preferredRateId\n        rateIdentifier\n        showRecommendation\n        suggestedNumOfRooms\n        status\n        __typename\n      }\n      hasNodateRooms\n      isAllInclusiveHotel\n      location {\n        neighborhoodDescription\n        __typename\n      }\n      hotelFeatures {\n        features\n        highlightedAmenities\n        hotelAmenities {\n          code\n          displayable\n          free\n          name\n          type\n          __typename\n        }\n        topAmenities\n        breakfastDetails\n        __typename\n      }\n      policies {\n        checkInTime\n        checkOutTime\n        petDescription\n        childrenDescription\n        importantInfo\n        __typename\n      }\n      itemKey\n      basketItemKey\n      componentKey\n      retailPrice {\n        pricePerPerson\n        displayPricePerPerson\n        amount\n        displayAmount\n        __typename\n      }\n      images {\n        imageHDURL\n        imageURL\n        __typename\n      }\n      __typename\n    }\n    componentKeyMap\n    los\n    signInDealRelatedInfo {\n      promptUserToSignIn\n      __typename\n    }\n    __typename\n  }\n}\n","variables":{"appCode":"DESKTOP","cguid":"b6a02daf29ebfcd2d3a1f83498e688da","checkIn":"20220523","checkOut":"20220527","rID":"DTDIRECT","roomsCount":1,"currencyCode":"USD","refClickID":"","unlockDeals":True,"includePrepaidFeeRates":True,"visitId":"20211028160655190c1a0d-RRLXGQD","addErrToResponse":True,"adults":2,"paymentRateMerge":False,"multiOccDisplay":True,"multiOccRates":True,"hotelID":"","rateDisplayOption":"S","reviewCount":5,"responseOptions":"POP_COUNT,REVIEWS,CUSTOM_DESC,RATE_SUMMARY,RATINGS,DETAILED_ROOM,HOTEL_IMAGES,RATE_IMPORTANT_INFO,RATE_CHARGES_DETAIL,PROXIMITY,BOOKINGS,NORATEROOMS,REFUND_INFO"},"operationName":"getHotelDetails"}

    try:
       os.remove('abx.csv')
    except OSError:
       pass
    # custom settings
    custom_settings = {
        'CONCURRENT_REQUEST_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1
    }

    urls = []

    results = []

    urls_id = []

    def __init__(self):
        with open('urls.txt', 'r') as text_file:
             for line in text_file.read().split('\n'):
                self.urls.append(line)

        for url in self.urls:
            try:
               hotel_id = url.split('/')[5]
               print(hotel_id)
               self.urls_id.append(hotel_id)

            except:
              pass

    # general crawler
    def start_requests(self):

          payload_id = self.payload['variables']['deals']

          for i in self.urls_id:
              #print(i)

              for j in payload_id:
                  j['dealId'] = i

                  yield scrapy.Request(
                      url = self.base_url,
                      body = json.dumps(self.payload),
                      method = "POST",
                      headers = self.headers2,
                      callback = self.parse,
                      dont_filter = True
                      )

    def parse(self, response):
       print(response.status)
       data = json.loads(response.body)

       data = data['data']['hotelContent']

       data = data['hotels']

       hotel_id3 = []

       for i in data:

           features = {
              'Name' : i['name'],
              'Address' : i['location']['neighborhoodName'],
              'Country' : i['location']['address']['countryName'],
              'Phone' : i['location']['address']['phone'],
              'Star_Rating' : i['starRating']
           }

           print(features)

       payload_id2 = self.payload2['variables']['hotelID']

       for i in self.urls_id:
          #print(i)
          '''
          for j in payload_id2:
              print('\n\npayload2 id \n\n',j['hotelID']) #= str(i)
          '''
          hotel_id2 = self.payload2['variables']['hotelID']
          hotel_id2 = str(i)
          #print(hotel_id2)

          print(self.payload2['variables']['hotelID'])

          yield scrapy.Request(
                  url = self.base_url,
                  body = json.dumps(self.payload2),
                  method = "POST",
                  headers = self.headers2,
                  callback = self.parse2,
                  dont_filter = True
                  )



    def parse2(self, response):
           data = json.loads(response.body)
           data = data['data']['details']

           data = data['hotel']

           data = data['ratesSummary']

           features = {
                 'Price' : data['minPrice'],
                 'Status' : data['status']
            }

           print(features)



           # append data to list
           self.results.append(features)

           header = features.keys()

           # store all the scraped data into csv file
           with open('hotels.csv', 'w+', newline = '') as csv_file:
              writer = csv.DictWriter(csv_file, fieldnames = header)
              writer.writeheader()
              writer.writerows(self.results)



if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Hotels)
    process.start()

    #Hotels.parse(Hotels.parse, '')
