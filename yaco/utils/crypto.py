import M2Crypto
import hashlib
import urllib
import base64

"""
Sign the data in the given dictionary and return a new hash
that includes the signature. 

@param $data Is a dictionary that contains the values to be signed
@param $salt Is the salt parameter passed via the cvm_salt GET parameter
@param $pkey Is the path to the private key file that will be used to calculate the signature
"""
def sign( data, salt, pkey ):

    # Calculate buffer to sign (sorting the keys)
    strBuffer = ""
    for k in sorted(data.iterkeys()):

        # Handle the BOOL special case
        v = data[k]
        if type(v) == bool:
            if v:
                v=1
            else:
                v=0
            data[k] = v

        # Update buffer
        strBuffer += "%s=%s\n" % ( str(k).lower(), urllib.quote(str(v)) )

    # Append salt
    strBuffer += salt

    # Sign data
    rsa = M2Crypto.RSA.load_key( pkey )
    digest = hashlib.new('sha512', strBuffer).digest()

    # Append signature
    data['signature'] = base64.b64encode( rsa.sign(digest, "sha512") )

    # Return new data dictionary
    return data
