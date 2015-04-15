import sublime, sublime_plugin


"""
How this works:
The point of this is to alphabetize all the attributes inside HTML tags in the entire 
selection. With this in mind, we need to first recognize we are in a tag and second find 
the attributes. 

All characters outside of a tag will be immediately added to the final HTML string 
because nothing needs to be ordered. 

Once inside a tag (when a [<] has been read), all characters that are not part of an 
attribute are added to a "markup" array (including spaces between attributes). All 
characters that are part of an attribute are added to an "attributes" array. When a [>] is 
read, we know we are finished with the tag. Because of this, we alphabetize the attributes 
array. Then, because of the spaces in between each attribute, we build a final tag string 
by alternating between first the "markup" array and second the "attributes" array until 
both are empty.

This final tag string is then appended to the final HTML string and the cycle repeats.
"""
class AlphabetizeAttrCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# Get all selected text
		sel = self.view.sel()
		# Loop through each region
		for region in sel:
			if len(region) > 0:
				# Get current region
				sub = self.view.substr(region)
				n = len(sub)
				# Set up universal counter
				i = 0
				# Initialize final HTML string
				finalHTML = ""

				# While there is still region left to search
				while i < n:
					########## OUTSIDE OF A TAG ##########

					# Search for an opening [<]
					while i < n and sub[i] != "<":
						finalHTML += sub[i] 
						i += 1

					# Now that we've found the end of the tag name,
					# we need to look for attributes. We know the attributes
					# and tag ends when [>] is found. Keep a flag that only
					# becomes False when this is found and the tag ends.
					if i < n:
						insideTag = True

					########## INSIDE A TAG ##########
					
					# Set up markup and attribute counters and arrays
					mi = 0
					ai = 0
					markup = []
					attributes = []
					# Keep strings for currently read characters for markup and attributes
					currMarkup = ""
					currAttr = ""

					# Search for the end of the tag name
					while sub[i] != " " and sub[i] != ">" and i < n:
						currMarkup += sub[i]
						i += 1
					
					# Loop through string until all attributes are found;
					# If looking at an attribute, add to the attribute array
					# Otherwise add to the normal markup array
					while i < n and insideTag:
						# Now we need to find an attribute or discover that the tag
						# has no attributes left.
						while i < n and insideTag and not sub[i].isalpha():
							curr = sub[i]
							currMarkup += sub[i]
							# If the end of the tag is found here, mark the tag as
							# finished
							if curr == ">":
								insideTag = False
							i += 1

						# We've hit the first attribute, so append to the markup array
						# and increment the markup array by 1
						markup.append(currMarkup)
						currMarkup = ""
						mi += 1

						# To determine if the attr will end with ['] or
						# ["], keep a var storing which type was found first and 
						# which to search for; keep a flag representing if the end
						# of an attribute is fournd
						searchFor = None
						insideAttr = True

						# Most attributes will end with ["] or ['] but just in
						# case it's a directive, search for spaces too
						while i < n and insideAttr and insideTag:
							curr = sub[i]

							# If a ['] or ["] is found
							if curr == "'" or curr == "\"":
								# If not already searching for something, start searching
								if searchFor == None:
									searchFor = curr
								# If it's the closing char we're looking for, stop searching
								elif curr == searchFor: 
									searchFor = None
								currAttr += curr
							# If a newline, slash, or space is found and we're not searching,
							# mark the attribute as finished and add to markup
							elif (curr == "\n" or 
								  curr == "/"  or
								  curr == " ") and searchFor == None:
								currMarkup = curr
								insideAttr = False
							# If a [>] is found and we're not searching,
							# mark the attribute and tag as finished and add to markup
							elif curr == ">" and searchFor == None:
								markup.append(curr)
								insideAttr = False
								insideTag = False
							# If none of the above cases, just add to the
							# attribute array and leave it at that
							else:
								currAttr += curr
							i += 1

						# We've hit the first attribute, so append to the attribute array
						# and increment the attribute array by 1
						if len(currAttr):
							attributes.append(currAttr)
							currAttr = ""
							ai += 1

					# Finished parsing into markup and attribute arrays, so 
					# move on to combination of arrays and alphabetization
					
					# Alphabetize the attributes only if we finished outside of
					# the tag
					if not insideTag:
						attributes.sort()

					# Use the markup state to alternate between the markup and
					# attribute arrays; will be True if we're pulling from markup array
					# and False if we're pulling from the attribute array
					markupIsCurr = True
					for j in range(len(markup) + len(attributes)):
						finalHTML += markup.pop(0) if markupIsCurr else attributes.pop(0)
						markupIsCurr = not markupIsCurr

			# Replace the original region			
			self.view.replace(edit, region, finalHTML)				