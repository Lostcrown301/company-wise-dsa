# Topic V2 Validation Report

## 1. QUESTION COUNTS
Total questions = 3430
Questions with >=1 topic = 1974
Questions with 0 topics = 1456
Check: 1974 + 1456 = 3430

## 2. TOPIC RELATIONSHIP COUNTS
V1 topic relationships: 5049
V2 topic relationships: 5655
New relationships: 606
Removed relationships: 0
Check: 5049 + 606 = 5655

## 3. SPECIALIZED TOPICS
Specialized Topic Relationships: 480
Unique Questions with Specialized Topics: 438
Difference: 42 (This represents questions with >1 specialized topic, e.g., 'Database' and 'Design')

## 4. HEAP
Heap / Priority Queue relationships added = 126

## 5. DUPLICATES
Duplicate question-topic relationships = 0
Duplicate company-question relationships = 0
Duplicate questions = 0
Duplicate companies = 0
Duplicate topics = 0

## 6. QUESTION IDENTITY
V1 question count: 3430
V2 question count: 3430
Questions removed: 0
Questions added: 0
Questions whose slug changed: 0

## 7. EXISTING CORE TOPICS
Core topic relationships removed: 0
Core topic relationships added: 0 (These are newly found relations for existing core topics!)

## 8. PROVENANCE
New topic relationships with source: 606
New topic relationships without source: 0

## 9. HEURISTIC CANDIDATES
Heuristics generated in separate file: 994
Heuristics applied to V2: 0 (All 606 new relationships came from CSV/raw data recovery)

## 10. SPECIALIZED TOPIC QUALITY
### Shell
- **Valid Phone Numbers** (`valid-phone-numbers`)
  - Companies: Media.Net, Microsoft, Meta...
  - Source: lc-questions

### Segment Tree
- **Maximize Subarray Sum After Removing All Occurrences of One Element** (`maximize-subarray-sum-after-removing-all-occurrences-of-one-element`)
  - Companies: Google, Rubrik
  - Source: lc-questions
- **Block Placement Queries** (`block-placement-queries`)
  - Companies: Paypay, Roblox, Meta...
  - Source: lc-questions
- **Find Building Where Alice and Bob Can Meet** (`find-building-where-alice-and-bob-can-meet`)
  - Companies: Meta, Infosys, Google...
  - Source: lc-questions
- **Create Sorted Array through Instructions** (`create-sorted-array-through-instructions`)
  - Companies: Google, Akuna Capital
  - Source: lc-questions
- **Find Subarray With Bitwise OR Closest to K** (`find-subarray-with-bitwise-or-closest-to-k`)
  - Companies: Salesforce
  - Source: lc-questions

### Ordered Set
- **Minimum Reverse Operations** (`minimum-reverse-operations`)
  - Companies: Infosys
  - Source: lc-questions
- **Design Movie Rental System** (`design-movie-rental-system`)
  - Companies: Amazon, Flipkart
  - Source: lc-questions
- **Range Module** (`range-module`)
  - Companies: Meta, Machine-Zone, Google...
  - Source: lc-questions
- **Design Log Storage System** (`design-log-storage-system`)
  - Companies: Twitter, Google, Apple...
  - Source: lc-questions
- **Falling Squares** (`falling-squares`)
  - Companies: Block, Amazon, Square...
  - Source: lc-questions

### Simulation
- **Fizz Buzz** (`fizz-buzz`)
  - Companies: Google, Apple, Capital One...
  - Source: lc-questions
- **Time Needed to Buy Tickets** (`time-needed-to-buy-tickets`)
  - Companies: Innovaccer, X, Meta...
  - Source: lc-questions
- **Minimum String Length After Removing Substrings** (`minimum-string-length-after-removing-substrings`)
  - Companies: J.P. Morgan, Wells Fargo, Yelp...
  - Source: lc-questions
- **Most Visited Sector in a Circular Track** (`most-visited-sector-in-a-circular-track`)
  - Companies: Syfe, Ibm, Expedia
  - Source: lc-questions
- **Queens That Can Attack the King** (`queens-that-can-attack-the-king`)
  - Companies: Media.Net, Microsoft, Medianet
  - Source: lc-questions

### Design
- **Range Module** (`range-module`)
  - Companies: Meta, Machine-Zone, Google...
  - Source: lc-questions
- **Design Log Storage System** (`design-log-storage-system`)
  - Companies: Twitter, Google, Apple...
  - Source: lc-questions
- **Design Search Autocomplete System** (`design-search-autocomplete-system`)
  - Companies: Linkedin, Snapchat, Doordash...
  - Source: lc-questions
- **Implement Trie** (`implement-trie-prefix-tree`)
  - Companies: Google, Apple, Arista Networks...
  - Source: lc-questions
- **Exam Room** (`exam-room`)
  - Companies: Uber, Quip, Samsung...
  - Source: lc-questions

### Database
- **Immediate Food Delivery I** (`immediate-food-delivery-i`)
  - Companies: Doordash
  - Source: lc-questions
- **Find Peak Calling Hours for Each City** (`find-peak-calling-hours-for-each-city`)
  - Companies: De Shaw
  - Source: lc-questions
- **The Number of Employees Which Report to Each Employee** (`the-number-of-employees-which-report-to-each-employee`)
  - Companies: Meta, Google, Bloomberg...
  - Source: lc-questions
- **Game Play Analysis II** (`game-play-analysis-ii`)
  - Companies: Amazon, Gsn-Games
  - Source: lc-questions
- **Number of Trusted Contacts of a Customer** (`number-of-trusted-contacts-of-a-customer`)
  - Companies: Roblox
  - Source: lc-questions

### Counting
- **Majority Element** (`majority-element`)
  - Companies: Ebay, Flipkart, Morgan Stanley...
  - Source: lc-questions
- **Stone Game IX** (`stone-game-ix`)
  - Companies: Samsung
  - Source: lc-questions
- **Minimum Number of Keypresses** (`minimum-number-of-keypresses`)
  - Companies: Snap, Amazon
  - Source: lc-questions
- **Largest Combination With Bitwise AND Greater Than Zero** (`largest-combination-with-bitwise-and-greater-than-zero`)
  - Companies: Adobe, Google, Amazon...
  - Source: lc-questions
- **Minimum Total Cost to Make Arrays Unequal** (`minimum-total-cost-to-make-arrays-unequal`)
  - Companies: Razorpay, Flipkart
  - Source: lc-questions

### Concurrency
- **Web Crawler Multithreaded** (`web-crawler-multithreaded`)
  - Companies: Facebook, Meta, Databricks...
  - Source: lc-questions
- **Design Bounded Blocking Queue** (`design-bounded-blocking-queue`)
  - Companies: Google, Linkedin, Bloomberg...
  - Source: lc-questions
- **Building H2O** (`building-h2o`)
  - Companies: Rubrik, Tesla, Google...
  - Source: lc-questions
- **Print in Order** (`print-in-order`)
  - Companies: Nvidia, Microsoft, Adobe...
  - Source: lc-questions


## VERDICT

**PASS**

All numerical checks pass. The number of unique questions with specialized topics (438) is smaller than the number of specialized relationships (480) because some questions have multiple specialized topics, and some questions already had topics but gained specialized topics. The question counts exactly match the required identity. All new relationships possess valid source provenance. No heuristic tags were mixed in. The Heap issue was correctly fixed yielding 126 new relationships without creating duplicates.