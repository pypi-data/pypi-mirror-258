
'''
{
	name: "feelings ECC 448 2: feel",
	fields:  {
		"showy rhythm": {
			"hexadecimal string": intimate_hexadecimal_string
		},
		"UTF8 string": story
	}
}

'''

	
import rich	

import reelity.modules.EEC_448_2.verify as verify
	

def performance (
	fields
):
	rich.print_json (data = fields)

	public_key_string = fields ["showy rhythm"] ["hexadecimal string"]

	verified = verify.start (
		public_key_string,
		
		signed_bytes = signed_bytes,
		unsigned_bytes = unsigned_bytes
	)

	return {
		"status": "pass",
		"note": {
			"feeling": ""
		}
	}