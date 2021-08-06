
#-----------------------------------------------------

userAgentKey = "User-Agent"
userAgentValue = ("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) " +
		"Gecko/20100101 Firefox/88.0")
#-----------------------------------------------------
acceptKey   = "Accept"
acceptValue = "*/*"
#-----------------------------------------------------
acceptLanguageKey   = "Accept-Language"
acceptLanguageValue = "en-US,en;q=0.5"
#-----------------------------------------------------
refererKey   = "Referer"
refererValue = "https://detectlanguage.com/"
#-----------------------------------------------------
contentTypeKey   = "Content-Type"
contentTypeValue = "application/json"
#-----------------------------------------------------
originKey   = "Origin"
originValue = "https://detectlanguage.com"
#-----------------------------------------------------
connectionKey   = "Connection"
connectionValue = "keep-alive"
#-----------------------------------------------------
# no cookies are required
#-----------------------------------------------------
teKey   = "TE"
teValue = "Trailers"
#-----------------------------------------------------
qKey = "q" # qValue is the text.
#-----------------------------------------------------

# google transtlate constants keys and values.

#-----------------------------------------------------

# request type should be POST, we are sending data
# with headers to Google servers.
requestType = "POST" # not optional




#-----------------------------------------------------

rpcKey   = "rpcids\u003d"
rpcValue = "MkEWBc"

#-----------------------------------------------------

rtKey   = "&rt\u003d"
rtValue = "c"

#-----------------------------------------------------

hlKey   = "&hl\u003d"
hlValue = "en-US"

#-----------------------------------------------------

sAppKey   = "&soc-app\u003d"
sAppValue = "1"

#-----------------------------------------------------

sPlatKey   = "&soc-pla\u0074form\u003d"
sPlatValue = "1"

#-----------------------------------------------------

sDevKey   = "&soc-device\u003d"
sDevValue = "1"

#-----------------------------------------------------

reqidKey   = "&\u005freqid\u003d"
reqidValue = "1662330"

#-----------------------------------------------------
#-----------------------------------------------------

sidKey   = "&f.sid\u003d"
sidValue = "-6960075458768589634"


#-----------------------------------------------------
blid  = "20210512.09"
wname = "-webserver"

blKey   = "&bl\u003d"
blValue = ("boq\u005f\u0074ransla\u0074e" + wname + "\u005f" + blid +
	"\u005fp0")


#-----------------------------------------------------


# WARNING: Do NOT edit this constant.
# In the query string we have:
#  * rpcids
#  * f.sid
#  * bl
#  * hl
#  * soc-app
#  * soc-platform
#  * soc-device
#  * _reqid
#  * rt
# and these are present in the request body (the raw data)
#  * f.req
#  * at
gHostUrl = (("\u0068\u0074\u0074ps\u003a\u002f\u002f\u0074" +
	"ransla\u0074e\u002e\u0067oo\u0067l\u0065\u002e\u0063o\u006d" + "\u002f") + 
	"\u005f\u002fTransla\u0074\u0065W\u0065bs\u0065rv\u0065rUi\u002fda\u0074a\u002f" + 
	"ba\u0074\u0063hex\u0065\u0063u\u0074e\u003f"
	+
	rpcKey + rpcValue +
	sidKey + sidKey +
	blKey + blValue +
	hlKey + hlValue +
	sAppKey + sAppValue +
	sPlatKey + sPlatValue +
	sDevKey + sDevValue +
	reqidKey + reqidValue +
	rtKey + rtValue) # not optional

# The Accept-Language request HTTP header advertises which languages
# the client is able to understand, and which locale variant is preferred.
# (By languages, we mean natural languages, such as English,
# and not programming languages.)
# Using content negotiation, the server then selects one of
# the proposals, uses it and informs the client of
# its choice with the Content-Language response header.
# Browsers set adequate values for this header according
# to their user interface language and even if a user can
# change it, this happens rarely (and is frowned upon as
# it leads to fingerprinting).
#
#  > see also: https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/Accept-Language
acceptLanguageGKey   = "Accept-Language"     # not optional
acceptLanguageGValue = "en-US,en;q\u003d0.5" # not optional

#-----------------------------------------------------

# The Referer HTTP request header contains an absolute or
# partial address of the page making the request.
# When following a link, this would be the address of the page
# containing the link.
# When making resource requests to another domain,
# this would be the address of the page using the resource.
# The Referer header allows servers to identify
# where people are visiting them from,
# which can then be used for analytics, logging, optimized caching, and more.
#
#  > see also: https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/Referer
refererGKey   = "Referer"                       # not optional
refererGValue = "https://translate.google.com/" # not optional

#-----------------------------------------------------

# same domain header field means we are sending the
# HTTP request to the same domain of our referer domain
# (and origin).
# we expect it to send us the respond using the same protocol.
# The same-origin policy is a critical security mechanism that
# restricts how a document or script loaded by one origin can interact with
# a resource from another origin.
# we should set its value to 1.
#
#  > see also: https://developer.mozilla.org/ja/docs/Web/Security/Same-origin_policy
xSameDomainGKey   = "X-Same-Domain" # not optional
xSameDomainGValue = "1"             # not optional

#-----------------------------------------------------

# For most of its major web apps,
# Google uses a batch-style RPC system that can be spotted
# by its common slug: batchexecute. At first glance,
# a request to this special API can seem hostile to
# anyone wanting an inside look.
# There are so many values to keep track of here,
# all of which are pretty opaque and strange.
# Luckily, finding them is not too difficult:
# Google sends all of them in a JavaScript object called WIZ.
xGoogBatchExecuteBgrGKey   = "X-Goog-BatchExecute-Bgr" # not optional
xGoogBatchExecuteBgrGValue = "" # not optional

#-----------------------------------------------------

# content type of our request should be
# application/x-www-form-urlencoded with charset of
# UTF8.
contentTypeGKey   = "Content-Type" # not optional
contentTypeGValue = ("application/x-www-form-urlencoded;" +
		"charset\u003dutf-8") # not optional

#-----------------------------------------------------

# The Origin request header indicates where a request originates
# from. It doesn't include any path information.
# It is similar to the Referer header,
# but, unlike that header, it doesn't disclose the whole path.
# Basically, browsers add the Origin request header to:
#  * all cross origin requests.
#  * same-origin requests except for GET or HEAD requests
#   (i.e. they are added to same-origin POST, OPTIONS,
#   PUT, PATCH, and DELETE requests).
#
#  > see also: https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/Origin
originGKey   = "Origin"                       # (not?) optional
originGValue = "https://translate.google.com" # (not?) optional

#-----------------------------------------------------

# I found this in their js code,
# it's optional but I prefer to use it in
# headers. I searched a bit in Qiita, but the only thing
# I found was some js code. anyway, since it works with it,
# let's set it to 1 in header fields.
#  > see also: https://en.wikipedia.org/wiki/Do_Not_Track
#  > see akso:
gDNTGKey   = "DNT" # optional
gDNTGValue = "1"   # optional

#-----------------------------------------------------

# the connection type should be keep-alive.
# we shouldn't get timeout, tho google is not
# slow in responding at all.
connectionGKey   = "Connection" # not optional
connectionGValue = "keep-alive" # not optional

#-----------------------------------------------------
# removed Cookie headers, since it will work without any cookie.
# I found this on medium:
# * NOTE: There may be a scenario in which you want to
# send a request unauthenticated.
# To do this, simply remove the Cookie header and
# the at value from your request.
# which is why I removed them.
#-----------------------------------------------------

# it's the body of the main request.
# it should contain the text we wanna translate.
# the value of the request is a three nested arrays.
# Let’s break them down one at a time.
# it should look like something like this (if you use urldecode):
# ```
#	[
#		[
#			[
#       		"rptSGc",
#        		"[[\"c8351307351755208604\"]]",
#				null,
#				"generic"
#			]
#		]
#	]
#
# * The first/outermost array simply holds the entire request.
#  This array will always have exactly one item,
#  which is the second array.
# * The second array contains each request in the batch.
#  We’re only sending one request with one payload,
#  so this array only has one item.
# * The third array is like an envelope for our payload,
#  describing when and where it should be sent.
#  Index 0 is our RPC ID, index 1 is the actual data being sent,
#  and index 3 describes in what order the payloads
#  should be processed. Because we only have one,
#  its value is "generic",
#  but if there were multiple it would start at "1"
#  and go upwards. The value at index 2 is always null.
#
#  > see also: https://qiita.com/kitauji/items/fdbd052c19dad28ab067
#  > see also: https://developers.google.com/protocol-buffers/docs/gotutorial#writing_a_message
#  > see also: https://kovatch.medium.com/deciphering-google-batchexecute-74991e4e446c
fReqGKey = "f.req\u003d" # not optional

DoubleQSP      = "\\\","
NonEscapeN     = "\\n"
NonEscapeNV    = "\\n,"
HttpRm         = "af.httprm"
E4Value        = "\"e\",4,"
NullCValue     ="null,"
GenericStr     = "," + "\"generic\""
NullCValueR    = "," + "null"
NeQ            = "\\n\""
NullN          = "\n\"" + "," + "null"
DiValue        = "\"di\""
AkCloseQ       = "}'"
WrbFr          = "\"wrb.fr\",\"MkEWBc\""
BoldOpen       = "\\u003cb\\u003e"
BoldClose      = "\\u003c/b\\u003e"
MiddleWave     = "\\\"," + "\\\""
WrongNessOpen  = """\\u003cb\\u003e\\u003ci\\u003e"""
WrongNessClose = """\\u003c/i\\u003e\\u003c/b\\u003e"""
ExampleFirst   = "null,\"\\u003cb\\u003e"
ThreeE         = "\\\\" + "u003e"
CeeE           = "\\\\" + "u003c"
QuetUnicode    = "u0026#39;"
StrAndCama     = "\\\","
StringAndCama  = "\","
CamaAndStr     = ",\\\""
NullAndCama    ="null,"
TwoCama        = ",,"
TwoStr         = "\"" + "\""
CamaNullCama   = ",null,"


LineChar   = '-' # line : '-'
EqualChar  = '=' # equal: '='
SpaceChar  = ' ' # space: ' '
DPointChar = ':' # double point: ':'

# router config values

GET_SLASH       = "/"
HTTP_ADDRESS    = ":"
FORMAT_VALUE    = "%v"
SPACE_VALUE     = " "
LineEscape      = "\n"
R_ESCAPE        = "\r"
SEMICOLON       = ";"
CAMA            = ","
ParaOpen        = "("
ParaClose       = ")"
NullStr         = "null"
SingleQ         = "'"
DoubleQJ        = "”"
BracketOpen     = "["
Bracketclose    = "]"
Star            = "*"
BackSlash       = "\\"
DoubleBackSlash = "\\\\"
Point           = "."
AutoStr         = "auto"
AtSign          = "@"
EqualStr        = "="
DdotSign        = ":"

# dynamic values

Verb = "verb"
Noun = "noun"


baseTwoIndex = 2
baseTenIndex = 10

badIgnore = '.' # always ignore this bad
bad01     = '?'
bad02     = '!'

forbiddenR01 = '\\'