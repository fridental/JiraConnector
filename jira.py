import sublime, sublime_plugin

tracing = True

class JiraReloadCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		#self.view.insert(edit, 0, "Hello, me!")
		#sublime.message_dialog("test")
		if tracing:
			print "Searching for jira issues in the current file"
		issues = parseJira(self.view)
		print str(len(issues)) + " jira issues found"

class JiraSaveCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		#self.view.insert(edit, 0, "Hello, me!")
		sublime.message_dialog("test")


class JiraIssue:
	def __init__(self, jira_id = None): 
		self.Id = jira_id
		self.TypeRegion = None
		self.FixVersionRegion = None
		self.ComponentRegion = None
		self.SummaryRegion = None
		self.DescriptionRegion = None
		self.LinkedFromRegion = None

	#def __str__(self):
	#	return "JIRA " + self.Component + "::" + self.FixVersion + "::" + self.Id + " " + self.Summary

def parseJira(view):
	issues = []
	cur_issue = None
	parsingProblems = False
	regs = view.find_all("^\\.[jira|type|fixversion|component|summary|description|linkedfrom|end]",sublime.IGNORECASE)	
	for i in range(0, len(regs)):
		if(i + 1 < len(regs)):
			end = regs[i + 1].begin()
		else:
			end = view.size()
		
		txt = view.substr(sublime.Region(regs[i].begin(),end))
		txt = txt.rstrip().rstrip("\n").rstrip();
		key = txt.lower()

		if key.startswith(".jira "):
			if cur_issue != None:
				issues.append(cur_issue)
			cur_issue = JiraIssue(txt[6:])

		if cur_issue == None:
			print "Unexpected '" + txt + "', no jira issue defined above"
			parsingProblems = True
			continue

		if key.startswith(".type "):
			cur_issue.TypeRegion = sublime.Region(regs[i].begin() + 6, end)

		if key.startswith(".fixversion "):
			cur_issue.FixVersionRegion = sublime.Region(regs[i].begin() + 12, end)

		if key.startswith(".component "):
			cur_issue.ComponentRegion = sublime.Region(regs[i].begin() + 11, end)

		if key.startswith(".summary "):
			cur_issue.SummaryRegion = sublime.Region(regs[i].begin() + 9, end)

		if key.startswith(".description "):
			cur_issue.DescriptionRegion = sublime.Region(regs[i].begin() + 13, end)

		if key.startswith(".linkedfrom "):
			cur_issue.LinkedFromRegion = sublime.Region(regs[i].begin() + 12, end)

		if key.startswith(".end"):
			if cur_issue != None:
				issues.append(cur_issue)
				cur_issue = None

	if cur_issue != None:
		issues.append(cur_issue)

	if parsingProblems:
		sublime.error_message("There were some parsing problems, check console for details.")

	return issues




