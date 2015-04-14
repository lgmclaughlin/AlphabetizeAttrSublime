import sublime, sublime_plugin

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
				# Set up counter
				i = 0
				# Set up markup and attribute counters and arrays
				mi = 0
				ai = 0
				markup = []
				attributes = []
				currMarkup = ""

				# Search for the opening [<]
				while i < n and sub[i] != "<":
					currMarkup += sub[i] 
					i += 1

				# Search for the end of the tag name
				while i < n and sub[i] != " ":
					currMarkup += sub[i]
					i += 1

				# Now that we've found the end of the tag name,
				# we need to look for attributes. We know the attributes
				# and tag ends when [>] is found. Keep a flag that only
				# becomes False when this is found and the tag ends.
				insideTag = True

				# Loop through string until all attributes are found;
				# If looking at an attribute, add to the attribute array
				# Otherwise add to the normal markup array
				while i < n and insideTag:
					# Skip over spaces
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

					currAttr = ""

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
						# If a space is found and we're not searching,
						# mark the attribute as finished and add to markup
						elif curr == " " and searchFor == None:
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

				# Finish adding the remaining string
				currMarkup = ""
				while i < n:
					currMarkup += sub[i]
					i += 1

				if len(currMarkup):
					markup[len(markup) - 1] += currMarkup

				# Finished parsing into markup and attribute arrays, so 
				# move on to combination of arrays and alphabetization
				attributes.sort()

				finalHTML = ""

				# Use the markup state to alternate between the markup and
				# attribute arrays; will be True if we're pulling from markup array
				# and False if we're pulling from the attribute array
				markupIsCurr = True
				for i in range(len(markup) + len(attributes)):
					finalHTML += markup.pop(0) if markupIsCurr else attributes.pop(0)
					markupIsCurr = not markupIsCurr

				# Make sure that the tag was finished, if not just return
				# the original substring
				self.view.replace(edit, region, sub) if insideTag else self.view.replace(edit, region, finalHTML)
