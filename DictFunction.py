from dateutil import parser


def add_values_in_dict(sample_dict, key, list_of_values):
        ''' Append multiple values to a key in
            the given dictionary '''
        if key not in sample_dict:
            sample_dict[key] = list()
        sample_dict[key].append(list_of_values)
        return sample_dict


def convertJSONtoDict(APIresponse, Dict, DateExtracted, SprintDay):
    startAt = APIresponse["startAt"]
    total = APIresponse["total"]
    for issue in range(min(total-startAt, 100)):
        add_values_in_dict(Dict, "Date Extracted", DateExtracted)

        projectName = APIresponse["issues"][issue]["fields"]["project"]
        if projectName == None:
            add_values_in_dict(Dict, "Project Name", projectName)
        else:
            projectName = APIresponse["issues"][issue]["fields"]["project"]["name"]
            add_values_in_dict(Dict, "Project Name", projectName)

        sprint = APIresponse["issues"][issue]["fields"]["customfield_10006"]
        if sprint == None:
            add_values_in_dict(Dict, "Sprint", sprint)
        else:
            sprints = []
            for s in range(0, len(APIresponse["issues"][issue]["fields"]["customfield_10006"])):
                sprints.append([int(n) for n in APIresponse["issues"][issue]["fields"]["customfield_10006"][s]["name"].split() if n.isdigit()])
            sprint = "Data Sprint " + str(max(sprints)[0])
            add_values_in_dict(Dict, "Sprint", sprint)

        add_values_in_dict(Dict, "Sprint Day", SprintDay)

        issueKey = APIresponse["issues"][issue]["key"]
        add_values_in_dict(Dict, "Issue Key", issueKey)

        issueType = APIresponse["issues"][issue]["fields"]["issuetype"]["name"]
        add_values_in_dict(Dict, "Issue Type", issueType)

        summary = APIresponse["issues"][issue]["fields"]["summary"]
        add_values_in_dict(Dict, "Summary", summary)

        assignee = APIresponse["issues"][issue]["fields"]["assignee"]
        assigneeId = APIresponse["issues"][issue]["fields"]["assignee"]
        if assignee == None:
            add_values_in_dict(Dict, "Assignee", assignee)
            add_values_in_dict(Dict, "Assignee Id", assigneeId)
        else:
            assignee = APIresponse["issues"][issue]["fields"]["assignee"]["displayName"]
            assigneeId = APIresponse["issues"][issue]["fields"]["assignee"]["accountId"]
            add_values_in_dict(Dict, "Assignee", assignee)
            add_values_in_dict(Dict, "Assignee Id", assigneeId)

        priority = APIresponse["issues"][issue]["fields"]["priority"]["name"]
        add_values_in_dict(Dict, "Priority", priority)

        status = APIresponse["issues"][issue]["fields"]["status"]["name"]
        add_values_in_dict(Dict, "Status", status)

        issueId = APIresponse["issues"][issue]["id"]
        add_values_in_dict(Dict, "Issue Id", issueId)

        epicLink = APIresponse["issues"][issue]["fields"]["customfield_10002"]
        add_values_in_dict(Dict, "Epic Link", epicLink)

        if "parent" in APIresponse["issues"][issue]["fields"] and APIresponse["issues"][issue]["fields"]["parent"]["fields"]["issuetype"]["name"] != "Epic":
            parentId = APIresponse["issues"][issue]["fields"]["parent"]["id"]
            parentSummary = APIresponse["issues"][issue]["fields"]["parent"]["fields"]["summary"]
            add_values_in_dict(Dict, "Parent Id", parentId)
            add_values_in_dict(Dict, "Parent Summary", parentSummary)
        else:
            parentId = None
            parentSummary = None
            add_values_in_dict(Dict, "Parent Id", parentId)
            add_values_in_dict(Dict, "Parent Summary", parentSummary)

        projectKey = APIresponse["issues"][issue]["fields"]["project"]["key"]
        add_values_in_dict(Dict, "Project Key", projectKey)

        component = APIresponse["issues"][issue]["fields"]["components"]
        if component == []:
            add_values_in_dict(Dict, "Component", None)
        else:
            component = APIresponse["issues"][issue]["fields"]["components"][0]["name"]
            add_values_in_dict(Dict, "Component", component)

        created = APIresponse["issues"][issue]["fields"]["created"]
        created = parser.parse(created).strftime("%d/%m/%Y %H:%M%p")
        add_values_in_dict(Dict, "Created", created)

        updated = APIresponse["issues"][issue]["fields"]["updated"]
        updated = parser.parse(updated).strftime("%d/%m/%Y %H:%M%p")
        add_values_in_dict(Dict, "Updated", updated)
        
        fixVersion = APIresponse["issues"][issue]["fields"]["fixVersions"]
        if fixVersion == []:
            add_values_in_dict(Dict, "Fix Version", None)
        else:
            fixVersion = APIresponse["issues"][issue]["fields"]["fixVersions"][0]["name"]
            add_values_in_dict(Dict, "Fix Version", fixVersion)

        originalEstimate = APIresponse["issues"][issue]["fields"]["timeoriginalestimate"]
        add_values_in_dict(Dict, "Original Estimate", originalEstimate)
        
        remainingEstimate = APIresponse["issues"][issue]["fields"]["timeestimate"]
        add_values_in_dict(Dict, "Remaining Estimate", remainingEstimate)

        storyPoints = APIresponse["issues"][issue]["fields"]["customfield_10100"]
        add_values_in_dict(Dict, "Story Points", storyPoints)
        

    return Dict


