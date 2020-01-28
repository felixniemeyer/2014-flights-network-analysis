module.exports = function splitSet(set) {

  let best_result = undefined
  let best_subsets = undefined

  let sorted_set = set.slice().sort((a,b) => a-b)

  for(let i = 1; i < sorted_set.length; i++) {
    let subsets = [
      sorted_set.slice(0, i),
      sorted_set.slice(i)
    ].map(s => ({ 
        elements: s,
        elements_sqrt: s.map(n => Math.sqrt(n))
      }))
  
    subsets.forEach(subset => {
      subset.distance = getDistance(subset.elements_sqrt)
      subset.mean = getMean(subset.elements)
   //   subset.Var = getVariance(subset.elements, subset.mean) 
   //   subset.deviation = Math.sqrt(subset.Var) 
   //   subset.deviationOvermean = subset.deviation / subset.mean
    })
    
    let result = subsets[0].distance + subsets[1].distance

    if(best_result === undefined || result < best_result) {
      best_result = result
      best_subsets = subsets
    }
  }
  return {
    lower_set: best_subsets[0].elements, 
    lower_mean: best_subsets[0].mean, 
    upper_set: best_subsets[1].elements,
    upper_mean: best_subsets[1].mean
  }
}

function getDistance(set) {
  let distance = 0
  for(x of set) {
    for(y of set) {
      distance += (x-y) * (x-y)
    }
  }
  return distance
}
    

function getMean(set) {
  return set.reduce((a, b) => a + b) / set.length
}

function getVariance(set, mean) {
  return set
    .map(a => Math.pow(mean - a, 2))
    .reduce((a, b) => a + b)
}
